import os
import asyncio
import json
import pathlib
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---- Load allowed enum lists from constants/ ----
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent  # project root


def _read_constant(filename: str):
    with open(BASE_DIR / "constants" / filename, "r", encoding="utf-8") as f:
        return json.load(f)


STYLES = _read_constant("cloth_style.json")["styles"]
MATERIALS = _read_constant("cloth_materials.json")["materials"]
COLORS = [
    c["name"]
    for palette in _read_constant("clothe_color.json")["color_palettes"].values()
    for c in palette
]
CATEGORIES = [
    item
    for sub in _read_constant("clothe_categories.json")["categories"].values()
    for item in sub
]
SEASONS = ["Spring", "Summer", "Fall", "Winter"]


# ---- Build OpenAI tool schema ----


def get_caption_tool_schema() -> dict:
    """Return the JSON schema definition for the structured caption tool."""
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


# ---- High-level helper to get structured caption via tool call ----


async def generate_structured_caption(image_url: str) -> dict | None:
    print("image_url", image_url)
    try:
        tools = [get_caption_tool_schema()]
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Look at the garment in the image and choose the correct category, "
                            "material, style, up to 3 dominant colours, suitable seasons, and craft "
                            "two texts: 'ai_context' (objective factual description WITHOUT mentioning that it's for AI) and 'brief_caption' (cool caption). "
                            "Return the result ONLY via the tool call."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url, "detail": "high"},
                    },
                ],
            }
        ]

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice={
                "type": "function",
                "function": {"name": "submit_cloth_caption"},
            },
        )

        assistant_msg = response.choices[0].message
        if assistant_msg.tool_calls:
            # take the first call (there will be exactly one)
            call = assistant_msg.tool_calls[0]
            args = json.loads(call.function.arguments)
            return args

        return None
    except Exception as error:
        print(f"Error in generate_structured_caption: {error}")
        return None


# Category-specific prompts for better captions
CATEGORY_PROMPTS = {
    "tops": "Analyze this clothing item and provide a detailed description focusing on the top/shirt. Describe the style, color, fabric texture, neckline, sleeves, and any unique features or patterns. Be specific about the garment type (e.g., blouse, t-shirt, sweater, tank top).",
    "longtops": "Analyze this clothing item and provide a detailed description focusing on the long top/dress. Describe the style, color, fabric texture, length, sleeves, neckline, and any unique features or patterns. Be specific about the garment type (e.g., maxi dress, tunic, long cardigan).",
    "bottoms": "Analyze this clothing item and provide a detailed description focusing on the bottom/pants. Describe the style, color, fabric texture, fit, length, and any unique features or patterns. Be specific about the garment type (e.g., jeans, skirt, shorts, trousers).",
    "one-pieces": "Analyze this clothing item and provide a detailed description focusing on the one-piece garment. Describe the style, color, fabric texture, fit, and any unique features or patterns. Be specific about the garment type (e.g., jumpsuit, romper, overall dress).",
    "shoes": "Analyze this footwear and provide a detailed description. Describe the style, color, material, heel height (if applicable), and any unique features or patterns. Be specific about the shoe type (e.g., sneakers, boots, sandals, heels).",
    "accessories": "Analyze this accessory and provide a detailed description. Describe the style, color, material, and any unique features or patterns. Be specific about the accessory type (e.g., bag, hat, jewelry, belt, scarf).",
}
