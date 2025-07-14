import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

from utils.caption_tools.caption_process_utils import clean_ai_context, clean_brief_caption
from utils.caption_tools.caption_utils import get_caption_tool_schema

load_dotenv()

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---- Caption generation via OpenAI tool call ----
async def generate_structured_caption(image_url: str) -> dict | None:
    print("image_url", image_url)
    #await asyncio.sleep(2)
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
        print(response)

        assistant_msg = response.choices[0].message
        print(assistant_msg)
        if assistant_msg.tool_calls:
            print("asdfasfdasfdasfasf")
            call = assistant_msg.tool_calls[0]
            args = json.loads(call.function.arguments)

            # Clean captions before returning
            args["ai_context"] = clean_ai_context(args["ai_context"])
            args["brief_caption"] = clean_brief_caption(args["brief_caption"])
            return args

        return None
    except Exception as error:
        print(f"Error in generate_structured_caption: {error}")
        return None

# ---- (Optional) Prompt templates for fine-tuning ----
CATEGORY_PROMPTS = {
    "tops": "Analyze this clothing item and provide a detailed description focusing on the top/shirt. Describe the style, color, fabric texture, neckline, sleeves, and any unique features or patterns. Be specific about the garment type (e.g., blouse, t-shirt, sweater, tank top).",
    "longtops": "Analyze this clothing item and provide a detailed description focusing on the long top/dress. Describe the style, color, fabric texture, length, sleeves, neckline, and any unique features or patterns. Be specific about the garment type (e.g., maxi dress, tunic, long cardigan).",
    "bottoms": "Analyze this clothing item and provide a detailed description focusing on the bottom/pants. Describe the style, color, fabric texture, fit, length, and any unique features or patterns. Be specific about the garment type (e.g., jeans, skirt, shorts, trousers).",
    "one-pieces": "Analyze this clothing item and provide a detailed description focusing on the one-piece garment. Describe the style, color, fabric texture, fit, and any unique features or patterns. Be specific about the garment type (e.g., jumpsuit, romper, overall dress).",
    "shoes": "Analyze this footwear and provide a detailed description. Describe the style, color, material, heel height (if applicable), and any unique features or patterns. Be specific about the shoe type (e.g., sneakers, boots, sandals, heels).",
    "accessories": "Analyze this accessory and provide a detailed description. Describe the style, color, material, and any unique features or patterns. Be specific about the accessory type (e.g., bag, hat, jewelry, belt, scarf).",
}
