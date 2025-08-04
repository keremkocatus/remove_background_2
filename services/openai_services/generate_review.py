import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

from utils.review_registery import update_review_registry
from utils.openai_tool import get_outfit_review_prompt, get_outfit_review_tool_schema


load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_outfit_review(image_url: str, roast_level: int ,job_id: str) -> dict | None:
    try:
        messages = get_outfit_review_prompt(image_url, roast_level)
        tools = get_outfit_review_tool_schema()

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools
        )

        tool_call = response.choices[0].message.tool_calls[0]
        return json.loads(tool_call.function.arguments)

    except Exception as error:
        update_review_registry(job_id, "status", "failed")
        print(f"Error in generate_outfit_review: {error}")
        return None
