import json

from typing import AsyncGenerator, Dict, List, Optional, Tuple
from collections import Counter
from loguru import logger
from google.adk.agents import SequentialAgent, ParallelAgent, BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai.types import Content, Part

from content_intelligence.agents.compliance_detector_agent.agent import (
    build_compliance_detector_agent,
)
from content_intelligence.agents.compliance_guard_agent.agent import (
    build_compliance_guard_agent,
)
from content_intelligence.agents.compliance_notes_formatter_agent.schema import (
    ProgrammeOutput,
    Programme,
    Annotation,
    ActionFlags,
    Confidence,
    CategoryInstance,
)

from content_intelligence.agents.retrying_agent.agent import wrap_llm_agents_with_retry

# -------------------------
# Utilities
# -------------------------

# Presence ranking for aggregation
_PRESENCE_RANK = {"Absent": 0, "Unclear": 1, "Present": 2}

# Neutral flags for synthesized/absent instances
NEUTRAL_FLAGS = ActionFlags(
    channel_check="n",
    support_material="n",
    legal_review_by="n/a",
    legal_reason="n/a",
    escalation_path="n/a",
)


def dump_model(m):
    return (
        m.model_dump()
        if hasattr(m, "model_dump")
        else (m.dict() if hasattr(m, "dict") else m)
    )


def category_presence(ann: Optional[Annotation]) -> str:
    """
    Reduce a category's instances to one label:
      Present if any instance Present;
      else Unclear if any Unclear;
      else Absent (no instances or all Absent).
    """
    if not ann or not getattr(ann, "instances", None):
        return "Absent"
    ps = [getattr(i, "presence", "Absent") for i in ann.instances]
    if any(p == "Present" for p in ps):
        return "Present"
    if any(p == "Unclear" for p in ps):
        return "Unclear"
    return "Absent"


def demote_instances(instances: List[CategoryInstance]) -> List[CategoryInstance]:
    """Demote confidence by one for all instances (mirrors old annotation-level demotion)."""
    out: List[CategoryInstance] = []
    for i in instances:
        data = dump_model(i)
        data["confidence"] = demote_confidence(i.confidence)
        out.append(CategoryInstance(**data))
    return out


def synthesize_absent_annotation(cat: str, note: Optional[str] = None) -> Annotation:
    """Create an Absent annotation with a single neutral instance."""
    return Annotation(
        category=cat,  # type: ignore[arg-type]
        instances=[
            CategoryInstance(
                presence="Absent",
                start_timecode=None,
                end_timecode=None,
                prominence=0,
                graphicness=0,
                imitability=0,
                distress=0,
                confidence="High",
                attributes={},
                action_flags=NEUTRAL_FLAGS,
                notes=(note or None),
            )
        ],
    )


def demote_confidence(c: Confidence) -> Confidence:
    """Drop confidence by one level, clamped at Low."""
    if c == "High":
        return "Medium"
    if c == "Medium":
        return "Low"
    return "Low"


def to_cat_map(po: ProgrammeOutput) -> Dict[str, Annotation]:
    return {a.category: a for a in po.annotations}


def pick_programme_meta(
    primary: Optional[Programme], fallback: Optional[Programme]
) -> Programme:
    # Prefer primary if provided; else fallback; else a minimal shell
    if isinstance(primary, Programme):
        return primary
    if isinstance(fallback, Programme):
        return fallback
    # minimal placeholder (fields required by schema)
    return Programme(
        programme_id="unknown",
        title="Untitled",
        genre="Unknown",
        slot="Unknown",
        uk_location="unk",
        children_present="unk",
        vulnerable_person="unk",
        notes=None,
    )


# -------------------------
# Pairwise (Detector + Guard) merge per run
# -------------------------


def merge_detector_guard(
    detector: ProgrammeOutput,
    guard: ProgrammeOutput,
) -> ProgrammeOutput:
    """
    Combine one detector + one guard ProgrammeOutput under the per-instance schema.
    Any discrepancy between their category-level conclusions → demote ALL instances for that category by 1.

    Discrepancy rules (category-level reduction):
    - If detector_presence == "Absent" and guard_presence == "Absent" → no discrepancy.
    - If detector has the category and guard omits it:
        * If detector_presence == "Absent" → discrepancy (expected guard to assert Absent).
        * Else no discrepancy.
    - If both have the category and their reduced presences aren't both Absent → discrepancy.
    - If only guard has the category (Absent) and detector omits → no discrepancy.
    """
    dmap = to_cat_map(detector)
    gmap = to_cat_map(guard)

    merged: List[Annotation] = []
    all_cats = set(dmap.keys()) | set(gmap.keys())

    for cat in sorted(all_cats):
        d_ann = dmap.get(cat)
        g_ann = gmap.get(cat)

        d_pres = category_presence(d_ann)
        g_pres = category_presence(g_ann)

        # Choose base (prefer detector payload richness when present)
        base = d_ann or g_ann
        if base is None:
            continue  # shouldn't happen

        # Determine discrepancy
        if d_ann and g_ann:
            discrepancy = not (d_pres == "Absent" and g_pres == "Absent")
        elif d_ann and not g_ann:
            discrepancy = d_pres == "Absent"
        else:  # g_ann and not d_ann
            discrepancy = False

        # Build instances from base; demote if discrepancy
        base_instances = base.instances if hasattr(base, "instances") else []
        new_instances = (
            demote_instances(base_instances)
            if discrepancy
            else [CategoryInstance(**dump_model(i)) for i in base_instances]
        )

        merged.append(
            Annotation(
                category=base.category,
                instances=new_instances,
            )
        )

    # Programme metadata – prefer detector, fallback to guard
    programme = pick_programme_meta(detector.programme, guard.programme)
    output = ProgrammeOutput(programme=programme, annotations=merged)
    logger.info(output)
    return output


# -------------------------
# Majority voting across 3 runs
# -------------------------


def majority_vote_three(runs: List[ProgrammeOutput]) -> ProgrammeOutput:
    """
    Consensus over three merged outputs (per-instance model).

    For each category in ANY run:
      - Reduce each run's category to one presence via category_presence().
      - Majority vote by label; tie-break by Present > Unclear > Absent.
      - Take the annotation (and its instances) from a run that matches the winning presence.
      - If there is any variance (not unanimous), demote ALL instances in the chosen annotation by 1.
      - If the winning presence is Absent and no run provided an annotation for that category,
        synthesize one neutral Absent annotation (single instance).
    """
    maps: List[Dict[str, Annotation]] = [to_cat_map(po) for po in runs]
    all_cats = set().union(*[m.keys() for m in maps])

    consensus_annotations: List[Annotation] = []

    def presence_vote_for_cat(
        cat: str,
    ) -> Tuple[str, List[str], List[Optional[Annotation]]]:
        pres: List[str] = []
        anns: List[Optional[Annotation]] = []
        for m in maps:
            ann = m.get(cat)
            anns.append(ann)
            pres.append(category_presence(ann))
        # Majority + tie-break
        counts = Counter(pres)
        most = counts.most_common()
        if len(most) == 1:
            winning = most[0][0]
        else:
            top_count = most[0][1]
            tied = [p for p, c in most if c == top_count]
            winning = max(tied, key=lambda p: _PRESENCE_RANK.get(p, 0))
        return winning, pres, anns

    for cat in sorted(all_cats):
        winning_presence, votes, anns_for_cat = presence_vote_for_cat(cat)

        # Pick a representative annotation from a run that matches the winning presence (by reduction)
        chosen_ann: Optional[Annotation] = None
        for ann in anns_for_cat:
            if ann and category_presence(ann) == winning_presence:
                chosen_ann = ann
                break

        if chosen_ann is None and winning_presence == "Absent":
            # No run held an Absent annotation; synthesize a neutral one
            chosen_ann = synthesize_absent_annotation(cat, note=None)

        if chosen_ann is None:
            # If still none (shouldn't happen), skip
            continue

        # Demote if any variance across runs
        unanimous = all(p == winning_presence for p in votes)
        instances = chosen_ann.instances
        new_instances = (
            demote_instances(instances)
            if not unanimous
            else [CategoryInstance(**dump_model(i)) for i in instances]
        )

        consensus_annotations.append(
            Annotation(category=chosen_ann.category, instances=new_instances)
        )

    # Programme metadata – prefer the first valid run
    programme = None
    for po in runs:
        if isinstance(po.programme, Programme):
            programme = po.programme
            break
    programme = programme or pick_programme_meta(None, None)

    output = ProgrammeOutput(programme=programme, annotations=consensus_annotations)
    logger.info(output)
    return output


# -------------------------
# Collector Agent (updated)
# -------------------------
class ProgrammeOutputCollectorAgent(BaseAgent):
    """
    1) For each suffix (1,2,3), merge the detector + guard outputs into a single ProgrammeOutput
       applying discrepancy demotions.
    2) Build a consensus over the 3 merged outputs via majority voting, demoting confidence where
       any variance exists across runs.

    Outputs written to state:
      - programme_output_combined_1 / _2 / _3
      - programme_output_consensus
      - programme_outputs_all (list of the 3 combined)
      - programme_outputs_all_dicts (JSON-serialisable)
    """


from typing import AsyncGenerator, List
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai.types import Content, Part


class ProgrammeOutputCollectorAgent(BaseAgent):
    async def _run_async_impl(
        self, context: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        logger.debug("Collector: starting _run_async_impl")

        state = context.session.state
        merged_runs: List[ProgrammeOutput] = []
        combined_keys: List[str] = []

        logger.debug(f"Collector: initial state keys = {list(state.keys())}")

        for suffix in ("1", "2", "3"):
            d_key = f"compliance_detector_agent_formatted_output_{suffix}"
            g_key = f"compliance_guard_agent_formatted_output_{suffix}"

            d_val = state.get(d_key)
            g_val = state.get(g_key)

            logger.debug(
                f"Collector: processing suffix={suffix} | "
                f"d_key={d_key}, g_key={g_key} | "
                f"d_val={'present' if d_val else 'missing'}, "
                f"g_val={'present' if g_val else 'missing'}"
            )

            if d_val is None and g_val is None:
                logger.warning(f"Collector: no outputs for suffix={suffix}; skipping")
                continue

            # Hydrate into ProgrammeOutput
            try:
                det_po = (
                    d_val
                    if isinstance(d_val, ProgrammeOutput)
                    else (ProgrammeOutput(**d_val) if d_val else None)
                )
                logger.debug(
                    f"Collector: detector ProgrammeOutput hydrated successfully for suffix={suffix}"
                )
            except Exception as e:
                logger.warning(f"Collector: malformed detector output {suffix}: {e}")
                det_po = None

            try:
                grd_po = (
                    g_val
                    if isinstance(g_val, ProgrammeOutput)
                    else (ProgrammeOutput(**g_val) if g_val else None)
                )
                logger.debug(
                    f"Collector: guard ProgrammeOutput hydrated successfully for suffix={suffix}"
                )
            except Exception as e:
                logger.warning(f"Collector: malformed guard output {suffix}: {e}")
                grd_po = None

            # Fill missing
            if det_po is None:
                logger.info(
                    f"Collector: missing detector output for suffix={suffix}, filling with defaults"
                )
                det_po = ProgrammeOutput(
                    programme=(
                        grd_po.programme if grd_po else pick_programme_meta(None, None)
                    ),
                    annotations=[],
                )

            if grd_po is None:
                logger.info(
                    f"Collector: missing guard output for suffix={suffix}, filling with defaults"
                )
                grd_po = ProgrammeOutput(
                    programme=(
                        det_po.programme if det_po else pick_programme_meta(None, None)
                    ),
                    annotations=[],
                )

            try:
                merged = merge_detector_guard(det_po, grd_po)
                merged_runs.append(merged)
                state[f"programme_output_combined_{suffix}"] = dump_model(merged)
                combined_keys.append(f"programme_output_combined_{suffix}")
                logger.debug(
                    f"Collector: successfully merged outputs for suffix={suffix}"
                )
            except Exception as e:
                logger.error(
                    f"Collector: failed to merge outputs for suffix={suffix}: {e}"
                )

        # Consensus if any runs merged
        if merged_runs:
            logger.info(
                f"Collector: {len(merged_runs)} run(s) merged successfully, building consensus"
            )
            try:
                consensus = majority_vote_three(merged_runs)
                consensus_dict = dump_model(consensus)
                state["programme_output_consensus"] = consensus_dict
                state["programme_outputs_all"] = merged_runs
                state["programme_outputs_all_dicts"] = [
                    dump_model(po) for po in merged_runs
                ]

                logger.info(
                    f"Collector: merged {len(merged_runs)} run(s) into consensus. "
                    f"Combined keys: {', '.join(combined_keys)}"
                )

                yield Event(
                    author=self.name or "programme_output_collector",
                    content=Content(
                        parts=[
                            Part(
                                text=json.dumps(
                                    {"output": consensus_dict}, indent=2, default=str
                                )
                            )
                        ],
                    ),
                )
            except Exception as e:
                logger.error(f"Collector: error during consensus generation: {e}")
                yield Event(
                    author=self.name or "programme_output_collector",
                    content=Content(parts=[Part(text=f"Error during consensus: {e}")]),
                )
        else:
            msg = "Collector: no valid runs to merge."
            logger.warning(msg)
            yield Event(
                author=self.name or "programme_output_collector",
                content=Content(parts=[Part(text=msg)]),
            )

        logger.debug("Collector: _run_async_impl complete")
        return


# ---------------------------------------------------------------------
# Build a per-suffix pipeline (detector + guard)
# ---------------------------------------------------------------------
def build_compliance_detector_guard_pipeline(suffix: str):
    detector_agent = build_compliance_detector_agent(suffix)
    guard_agent = build_compliance_guard_agent(suffix)

    return ParallelAgent(
        name=f"compliance_detector_guard_pipeline_{suffix}",
        sub_agents=[detector_agent, guard_agent],
    )


# ---------------------------------------------------------------------
# Build the full parallel pipeline + collector
# ---------------------------------------------------------------------
def get_pipeline() -> BaseAgent:
    p1 = build_compliance_detector_guard_pipeline("1")
    p2 = build_compliance_detector_guard_pipeline("2")
    p3 = build_compliance_detector_guard_pipeline("3")

    parallel = ParallelAgent(
        name="compliance_detector_guard_parallel",
        sub_agents=[
            p1,
            p2,
            # p3
        ],
    )
    collector = ProgrammeOutputCollectorAgent(name="programme_output_collector")

    pipeline = SequentialAgent(
        name="compliance_pipeline_with_collector",
        sub_agents=[parallel, collector],
    )

    pipeline_with_retry = wrap_llm_agents_with_retry(
        pipeline,
        max_429_retries=2,  # single retry for 429; Vertex queues automatically
        base_delay_429=1.0,  # minimal wait (s)
        max_transient_retries=2,  # at most two transient retries (5xx/UNAVAILABLE)
        base_delay_transient=1.0,  # smaller base delay
        backoff=1.5,  # gentler exponential increase
        max_delay=5.0,  # cap backoff at 10s (vs. 32s)
        pt_overage_policy="allow_spillover",  # continue to allow spillover to PayGo
    )

    return pipeline_with_retry


# ---------------------------------------------------------------------
# Example runner
# ---------------------------------------------------------------------
if __name__ == "__main__":
    from content_intelligence.runner import run_pipeline

    APP_NAME = "compliance_tagging_demo"
    test_gcs_uri = "gs://compliance-poc-videos/M2428051-1080-7830.mp4"

    logger.info("Starting video description test...")
    pipeline = get_pipeline()
    result = run_pipeline(pipeline, APP_NAME, test_gcs_uri)
    logger.success(result)
