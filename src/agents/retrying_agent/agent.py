import asyncio
import random
import re
from typing import AsyncGenerator, Optional, Literal

from loguru import logger
from pydantic import ConfigDict
from google.adk.agents import BaseAgent, LlmAgent, SequentialAgent, ParallelAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai import errors as genai_errors
from google.genai.types import Content, Part


# ---------- utilities ----------
def _sanitize_agent_id(name: str) -> str:
    s = re.sub(r"\W+", "_", name or "agent")
    if not re.match(r"^[A-Za-z_]", s):
        s = f"a_{s}"
    return s


def _content(msg: str) -> Content:
    return Content(parts=[Part(text=msg)])


# ---------- Retrying wrapper ----------
class RetryingAgent(BaseAgent):
    """
    Pydantic-safe retry wrapper around any BaseAgent with Loguru logging.
    - Retries 429 at most 2 times with 1s min delay (per Google doc).
    - Retries transient 5xx/UNAVAILABLE a few times with backoff.
    - Optionally hints spillover to PayGo by writing a state flag when PT 429 is detected.
    """

    # Pydantic config
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Declare fields (Pydantic!)
    inner: BaseAgent

    # Retry policy fields
    max_429_retries: int = 2
    base_delay_429: float = 1.0
    max_transient_retries: int = 5
    base_delay_transient: float = 2.0
    backoff: float = 2.0
    max_delay: float = 32.0
    pt_overage_policy: Literal["allow_spillover", "no_change"] = "allow_spillover"

    async def _run_async_impl(
        self, context: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        attempts_429 = 0
        attempts_transient = 0
        delay_429 = self.base_delay_429
        delay_transient = self.base_delay_transient

        logger.debug(
            "[{}] starting; inner='{}', 429(max={},base_delay={}s), transient(max={},base_delay={}s), backoff={} max_delay={}s, pt_policy={}",
            self.name,
            getattr(self.inner, "name", type(self.inner).__name__),
            self.max_429_retries,
            self.base_delay_429,
            self.max_transient_retries,
            self.base_delay_transient,
            self.backoff,
            self.max_delay,
            self.pt_overage_policy,
        )

        while True:
            try:
                logger.debug(
                    "[{}] invoking inner agent '{}'",
                    self.name,
                    getattr(self.inner, "name", type(self.inner).__name__),
                )
                async for ev in self.inner.run_async(context):
                    yield ev
                logger.debug(
                    "[{}] inner '{}' completed successfully",
                    self.name,
                    getattr(self.inner, "name", type(self.inner).__name__),
                )
                return

            except Exception as e:
                code = getattr(e, "code", None)
                status = getattr(e, "status", None)
                text = (str(e) or "").lower()

                # ----- 429 handling -----
                if code == 429 or any(
                    t in text
                    for t in ["resource exhausted", "too many requests", "quota"]
                ):
                    attempts_429 += 1
                    logger.warning(
                        "[{}] '{}' -> 429/RESOURCE_EXHAUSTED (attempt {}/{}) | status={} code={} | msg={}",
                        self.name,
                        getattr(self.inner, "name", type(self.inner).__name__),
                        attempts_429,
                        self.max_429_retries,
                        status,
                        code,
                        str(e).strip(),
                    )

                    if attempts_429 > self.max_429_retries:
                        logger.error(
                            "[{}] giving up on 429 after {} attempts for '{}'",
                            self.name,
                            attempts_429 - 1,
                            getattr(self.inner, "name", type(self.inner).__name__),
                        )
                        raise

                    # If this looks like Provisioned Throughput overage, hint spillover
                    if (
                        "provisioned throughput" in text
                        and self.pt_overage_policy == "allow_spillover"
                    ):
                        context.session.state["__advice_request_type__"] = "shared"
                        logger.info(
                            "[{}] PT overage detected; setting __advice_request_type__='shared' to allow spillover on next attempt",
                            self.name,
                        )

                    wait = delay_429
                    logger.debug(
                        "[{}] scheduling 429 retry in ~{:.2f}s (next backoff -> {:.2f}s)",
                        self.name,
                        wait,
                        min(self.max_delay, delay_429 * self.backoff),
                    )
                    yield Event(
                        author=self.name,
                        content=_content(
                            f"{getattr(self.inner, 'name', type(self.inner).__name__)} 429; retry {attempts_429}/{self.max_429_retries} in ~{wait:.1f}s"
                        ),
                    )
                    await asyncio.sleep(wait + wait * 0.25 * random.random())
                    delay_429 = min(self.max_delay, delay_429 * self.backoff)
                    continue

                # ----- 5xx / UNAVAILABLE handling -----
                is_server_err = isinstance(
                    e, (genai_errors.ServerError, genai_errors.APIError)
                )
                looks_transient = (
                    (code in (500, 503))
                    or status == "UNAVAILABLE"
                    or ("server error" in text)
                    or ("unavailable" in text)
                )
                if is_server_err and looks_transient:
                    attempts_transient += 1
                    logger.warning(
                        "[{}] '{}' -> transient error (attempt {}/{}) | status={} code={} | msg={}",
                        self.name,
                        getattr(self.inner, "name", type(self.inner).__name__),
                        attempts_transient,
                        self.max_transient_retries,
                        status,
                        code,
                        str(e).strip(),
                    )
                    if attempts_transient > self.max_transient_retries:
                        logger.error(
                            "[{}] giving up on transient error after {} attempts for '{}'",
                            self.name,
                            attempts_transient - 1,
                            getattr(self.inner, "name", type(self.inner).__name__),
                        )
                        raise

                    wait = delay_transient
                    logger.debug(
                        "[{}] scheduling transient retry in ~{:.2f}s (next backoff -> {:.2f}s)",
                        self.name,
                        wait,
                        min(self.max_delay, delay_transient * self.backoff),
                    )
                    yield Event(
                        author=self.name,
                        content=_content(
                            f"{getattr(self.inner, 'name', type(self.inner).__name__)} transient; retry {attempts_transient}/{self.max_transient_retries} in ~{wait:.1f}s"
                        ),
                    )
                    await asyncio.sleep(wait + wait * 0.25 * random.random())
                    delay_transient = min(
                        self.max_delay, delay_transient * self.backoff
                    )
                    continue

                # Non-retryable → bubble up
                logger.exception(
                    "[{}] non-retryable error from inner '{}' | status={} code={} | msg={}",
                    self.name,
                    getattr(self.inner, "name", type(self.inner).__name__),
                    status,
                    code,
                    str(e).strip(),
                )
                raise


# ---------- recursive wrapper ----------
def wrap_llm_agents_with_retry(agent: BaseAgent, **retry_kwargs) -> BaseAgent:
    """
    Recursively wrap LlmAgent leaves with RetryingAgent.
    Return a (possibly) new tree; do not mutate names into invalid identifiers.
    Adds debug logging to show wrapping decisions.
    """
    if isinstance(agent, LlmAgent):
        safe_inner_name = _sanitize_agent_id(
            getattr(agent, "name", agent.__class__.__name__)
        )
        wrapper_name = f"retry_{safe_inner_name}"
        logger.debug(
            "[wrap] wrapping LlmAgent '{}' -> '{}' with kwargs={} ",
            safe_inner_name,
            wrapper_name,
            retry_kwargs,
        )
        return RetryingAgent(inner=agent, name=wrapper_name, **retry_kwargs)

    if isinstance(agent, SequentialAgent):
        logger.debug(
            "[wrap] descending into SequentialAgent '{}' ({} sub-agents)",
            getattr(agent, "name", "sequential"),
            len(agent.sub_agents),
        )
        agent.sub_agents = [
            wrap_llm_agents_with_retry(a, **retry_kwargs) for a in agent.sub_agents
        ]
        return agent

    if isinstance(agent, ParallelAgent):
        logger.debug(
            "[wrap] descending into ParallelAgent '{}' ({} sub-agents)",
            getattr(agent, "name", "parallel"),
            len(agent.sub_agents),
        )
        agent.sub_agents = [
            wrap_llm_agents_with_retry(a, **retry_kwargs) for a in agent.sub_agents
        ]
        return agent

    logger.debug(
        "[wrap] leaving non-LLM agent '{}' unchanged",
        getattr(agent, "name", type(agent).__name__),
    )
    return agent
