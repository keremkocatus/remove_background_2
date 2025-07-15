import asyncio
from supabase import AsyncClient
from dotenv import load_dotenv
from services.openai_services.openai_service import generate_structured_caption
import os

from services.supabase_services.insert_service import insert_clothes_detail

load_dotenv()
BUCKET_NAME = os.getenv("WARDROBE_BUCKET_NAME")

# Lazy-initialized Supabase client (reuses the one from supabase_wardrobe_service)
_supabase_client: AsyncClient | None = None
_supabase_lock = asyncio.Lock()

async def get_supabase_client() -> AsyncClient:
    from services.supabase_services.client_service import get_supabase_client as _get
    return await _get()

async def get_caption_for_image(job: dict):
    """
    Retrieve existing caption or generate a new one via ChatGPT and save it.

    Args:
        image_url: URL of the image to caption
        category: Clothing category for context

    Returns:
        The caption text
    """
    try:
        # Generate a caption using OpenAI
        caption = await generate_structured_caption(job["image_url"])

        await insert_clothes_detail(job["wardrobe_id"], job["user_id"], caption)

        # Save/update caption in Supabase
        supabase: AsyncClient = await get_supabase_client()
        
        resp = await supabase.from_(BUCKET_NAME).update({
            "caption": caption["ai_context"],
            "caption_status": "finished"
        }).eq("image_url", job["image_url"]).execute()

        return caption
    except Exception as e:
        print(f"Caption service error: {e}")
        return "Error generating caption"
