"""
Model selection utility that automatically detects available API credentials
and returns the appropriate LLM model configuration.
"""

import os
from typing import Optional, Union
from loguru import logger
from google.adk.models.lite_llm import LiteLlm, LiteLLMClient


def select_model(
    model_preference: Optional[str] = None,
) -> Union[LiteLlm, str]:
    """
    Automatically select and configure an LLM model based on available API credentials.

    Priority order (if model_preference not specified):
    1. Azure OpenAI (if AZURE_DEPLOYMENT_NAME is set)
    2. OpenAI (if OPENAI_API_KEY is set)
    3. Gemini (if GEMINI_API_KEY is set)

    Args:
        model_preference: Optional string to force a specific provider.
                         Options: "azure", "openai", "gemini"

    Returns:
        LiteLlm instance or model string for the selected provider

    Raises:
        ValueError: If no valid API credentials are found

    Note:
        Temperature should be set individually in each agent's generate_content_config.
    """

    # Check Azure
    azure_deployment = os.getenv("AZURE_DEPLOYMENT_NAME")
    azure_api_key = os.getenv("AZURE_API_KEY")
    azure_api_base = os.getenv("AZURE_API_BASE")

    # Check OpenAI
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Check Gemini
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    # If preference specified, validate and use it
    if model_preference:
        model_preference = model_preference.lower()

        if model_preference == "azure":
            if not all([azure_deployment, azure_api_key, azure_api_base]):
                raise ValueError(
                    "Azure preference specified but missing required environment variables: "
                    "AZURE_DEPLOYMENT_NAME, AZURE_API_KEY, AZURE_API_BASE"
                )
            logger.info(f"Using Azure OpenAI deployment: {azure_deployment}")
            return LiteLlm(
                model=f"azure/{azure_deployment}", llm_client=LiteLLMClient()
            )

        elif model_preference == "openai":
            if not openai_api_key:
                raise ValueError(
                    "OpenAI preference specified but OPENAI_API_KEY not found"
                )
            # Default to gpt-4o-mini if using OpenAI
            model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            logger.info(f"Using OpenAI model: {model_name}")
            return LiteLlm(model=model_name, llm_client=LiteLLMClient())

        elif model_preference == "gemini":
            if not gemini_api_key:
                raise ValueError(
                    "Gemini preference specified but GEMINI_API_KEY not found"
                )
            # Default to gemini-2.0-flash-exp if using Gemini
            model_name = os.getenv("GEMINI_MODEL", "gemini/gemini-2.0-flash-exp")
            logger.info(f"Using Gemini model: {model_name}")
            return model_name

        else:
            raise ValueError(
                f"Invalid model_preference: {model_preference}. "
                "Must be one of: 'azure', 'openai', 'gemini'"
            )

    # Auto-detect based on priority
    if all([azure_deployment, azure_api_key, azure_api_base]):
        logger.info(f"Auto-detected Azure OpenAI deployment: {azure_deployment}")
        return LiteLlm(model=f"azure/{azure_deployment}", llm_client=LiteLLMClient())

    elif openai_api_key:
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        logger.info(f"Auto-detected OpenAI model: {model_name}")
        return LiteLlm(model=model_name, llm_client=LiteLLMClient())

    elif gemini_api_key:
        model_name = os.getenv("GEMINI_MODEL", "gemini/gemini-2.0-flash-exp")
        logger.info(f"Auto-detected Gemini model: {model_name}")
        return model_name

    else:
        raise ValueError(
            "No valid API credentials found. Please set one of:\n"
            "  - AZURE_DEPLOYMENT_NAME, AZURE_API_KEY, AZURE_API_BASE (for Azure)\n"
            "  - OPENAI_API_KEY (for OpenAI)\n"
            "  - GEMINI_API_KEY (for Gemini)"
        )


def get_model_info() -> dict:
    """
    Get information about the currently configured model.

    Returns:
        Dictionary with model provider and configuration details
    """
    azure_deployment = os.getenv("AZURE_DEPLOYMENT_NAME")
    azure_api_key = os.getenv("AZURE_API_KEY")
    azure_api_base = os.getenv("AZURE_API_BASE")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    info = {
        "providers_available": [],
        "default_provider": None,
        "model": None,
    }

    if all([azure_deployment, azure_api_key, azure_api_base]):
        info["providers_available"].append("azure")
        if not info["default_provider"]:
            info["default_provider"] = "azure"
            info["model"] = f"azure/{azure_deployment}"

    if openai_api_key:
        info["providers_available"].append("openai")
        if not info["default_provider"]:
            info["default_provider"] = "openai"
            info["model"] = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if gemini_api_key:
        info["providers_available"].append("gemini")
        if not info["default_provider"]:
            info["default_provider"] = "gemini"
            info["model"] = os.getenv("GEMINI_MODEL", "gemini/gemini-2.0-flash-exp")

    return info
