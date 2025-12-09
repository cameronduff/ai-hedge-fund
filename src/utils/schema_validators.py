"""
Common Pydantic validators for handling LLM outputs.
"""

import re
import json
from typing import Any


def strip_markdown_fences(data: Any) -> Any:
    """
    Strip markdown code fences if the LLM wraps JSON in them.

    This validator handles cases where LLMs return responses like:
    ```json
    {"key": "value"}
    ```

    Instead of raw JSON.

    Args:
        data: Input data that might be a string with markdown fences

    Returns:
        Parsed JSON dict if string, otherwise original data
    """
    if isinstance(data, str):
        # Remove markdown code fences like ```json ... ``` or ``` ... ```
        fence_pattern = re.compile(
            r"```(?:json)?\s*\n?(.*?)\n?```", re.DOTALL | re.IGNORECASE
        )
        match = fence_pattern.search(data)
        if match:
            json_str = match.group(1).strip()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        # Try to parse the string directly as JSON
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            pass
    return data
