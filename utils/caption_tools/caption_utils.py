import pathlib
import json

from utils.caption_tools.enum_utils import (
    extract_color_names_from_palette,
    extract_materials,
    extract_styles,
)

# ---- Load allowed enum lists from constants/ ----
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

def _read_constant(filename: str):
    with open(BASE_DIR / "constants" / filename, "r", encoding="utf-8") as f:
        return json.load(f)

STYLES = extract_styles(_read_constant("cloth_style.json"))
MATERIALS = extract_materials(_read_constant("cloth_materials.json"))
COLORS = extract_color_names_from_palette(_read_constant("clothe_color.json")["color_palettes"])
CATEGORIES = [
    item
    for sub in _read_constant("clothe_categories.json")["categories"].values()
    for item in sub
]
SEASONS = ["Spring", "Summer", "Fall", "Winter"]

# ---- OpenAI tool schema ----
def get_caption_tool_schema() -> dict:
    return {
        "type": "function",
        "function": {
            "name": "submit_cloth_caption",
            "description": (
                "Return a structured description for a clothing item in the image. "
                "Every categorical field MUST be chosen from the provided enum arrays. "
                "Additionally, provide two text snippets: \n"
                "1) ai_context -> long factual description for chatbot memory (not shown to user) \n"
                "2) brief_caption -> short cool caption for user (max 2 sentences, emojis allowed)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "enum": CATEGORIES},
                    "material": {"type": "string", "enum": MATERIALS},
                    "style": {"type": "string", "enum": STYLES},
                    "colors": {
                        "type": "array",
                        "items": {"type": "string", "enum": COLORS},
                        "minItems": 1,
                        "maxItems": 3,
                    },
                    "seasons": {
                        "type": "array",
                        "items": {"type": "string", "enum": SEASONS},
                        "minItems": 1,
                        "maxItems": 2,
                    },
                    "ai_context": {
                        "type": "string",
                        "description": (
                            "1–3 complete sentences giving a factual, objective description of the garment (colour tone, material feel, cut, notable details). "
                            "This will be stored in chatbot memory. Do NOT include any meta-comments or the phrase 'for AI'."
                        ),
                    },
                    "brief_caption": {
                        "type": "string",
                        "description": "Short, engaging caption for the user (<=2 sentences, emojis allowed).",
                    },
                },
                "required": [
                    "category",
                    "material",
                    "style",
                    "colors",
                    "seasons",
                    "ai_context",
                    "brief_caption",
                ],
            },
        },
    }