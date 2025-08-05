import asyncio
import os
from supabase import AsyncClient
from dotenv import load_dotenv

from services.openai_services.generate_caption import generate_structured_caption
from services.supabase_services.insert_service import insert_clothes_detail
from utils.wardrobe_registery import update_registry, get_job_id_by_job

load_dotenv()
BUCKET_NAME = os.getenv("WARDROBE_BUCKET_NAME")

async def get_supabase_client() -> AsyncClient:
    from services.supabase_services.client_service import get_supabase_client as _get
    return await _get()

async def process_caption_for_job(job: dict) -> dict | str:
    """
    Generates an AI-based outfit caption for the given job,
    stores it in Supabase and updates related registries.

    Args:
        job (dict): A job dict containing wardrobe_id, user_id, image_url, etc.

    Returns:
        dict: Generated caption object (structured)
        str: "Error generating caption" in case of failure
    """
    try:
        # 1. Generate caption using OpenAI
        caption_data = await generate_structured_caption(job["image_url"])

        # 2. Save to clothes detail table
        await insert_clothes_detail(
            wardrobe_id=job["wardrobe_id"],
            user_id=job["user_id"],
            caption=caption_data
        )

        # 3. Update registry
        job_id = get_job_id_by_job(job)
        update_registry(job_id, "caption_status", "finished")

        # 4. Update Supabase wardrobe entry
        supabase = await get_supabase_client()
        await supabase.from_(BUCKET_NAME).update({
            "caption": caption_data["ai_context"],
            "caption_status": "finished"
        }).eq("image_url", job["image_url"]).execute()

        return caption_data

    except Exception as e:
        print(f"[Caption Service] Error: {e}")
        return "Error generating caption"
