import re
from typing import Dict

def clean_ai_context(ai_context: str) -> str:
    """
    Remove unnecessary whitespace and make sure the context ends with a period.
    """
    cleaned = ai_context.strip()
    if not cleaned.endswith("."):
        cleaned += "."
    return cleaned

def clean_brief_caption(caption: str) -> str:
    """
    Normalize caption: remove extra spaces and limit to 2 sentences max.
    Emojis are preserved.
    """
    # Normalize whitespace
    caption = re.sub(r"\s+", " ", caption).strip()

    # Split into sentences and trim to 2
    sentences = re.split(r"(?<=[.!?])\s+", caption)
    return " ".join(sentences[:2])

def summarize_caption_data(data: Dict) -> str:
    """
    Converts the structured caption dict into a readable summary string (for logging or admin panel).
    """
    return (
        f"{data.get('style', 'Unknown')} {data.get('material', '')} "
        f"{data.get('category', '')} in {', '.join(data.get('colors', []))} "
        f"for {', '.join(data.get('seasons', []))}.\n"
        f"→ {data.get('brief_caption', '')}"
    )
