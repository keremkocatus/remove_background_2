import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_outfit_review(image_url: str) -> dict | None:
    try:
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "You're a fashion expert AI. Look at the outfit in the image and return a JSON object containing:\n"
                            "- 'review': a short paragraph giving overall impression of the outfit\n"
                            "- 'style_rating': score out of 5\n"
                            "- 'color_match_rating': score out of 5\n"
                            "- 'piece_match_rating': score out of 5\n"
                            "- 'overall_rating': score out of 5 (not average — your own holistic judgment)\n\n"
                            "Be honest but constructive. Output ONLY via tool call with the exact structure."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url, "detail": "high"}
                    }
                ]
            }
        ]

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "return_outfit_review",
                        "description": "Returns structured review and scores for an outfit",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "review": {"type": "string"},
                                "style_rating": {"type": "number"},
                                "color_match_rating": {"type": "number"},
                                "piece_match_rating": {"type": "number"},
                                "overall_rating": {"type": "number"}
                            },
                            "required": [
                                "review",
                                "style_rating",
                                "color_match_rating",
                                "piece_match_rating",
                                "overall_rating"
                            ]
                        }
                    }
                }
            ],
            tool_choice={"type": "function", "function": {"name": "return_outfit_review"}}
        )

        tool_call = response.choices[0].message.tool_calls[0]
        return json.loads(tool_call.function.arguments)

    except Exception as error:
        print(f"Error in generate_outfit_review: {error}")
        return None
