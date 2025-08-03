import asyncio
import os
from supabase import AsyncClient
from dotenv import load_dotenv

from services.openai_services.generate_review import generate_outfit_review
from services.supabase_services.insert_service import insert_outfit_review_detail
from utils.wardrobe_registery import update_registry, get_job_id_by_job

load_dotenv()
REVIEW_TABLE = os.getenv("REVIEW_TABLE")

async def get_supabase_client() -> AsyncClient:
    from services.supabase_services.client_service import get_supabase_client as _get
    return await _get()

async def process_outfit_review_for_job(job: dict) -> dict | str:
    """
    Generates a structured outfit review based on an image, stores the review in Supabase,
    and updates the related registry.

    Args:
        job (dict): A job dict containing wardrobe_id, user_id, image_url, etc.

    Returns:
        dict: Structured outfit review data
        str : "Error generating review" if something goes wrong
    """
    try:
        # 1. Generate outfit review using OpenAI
        review_data = await generate_outfit_review(job["image_url"])

        # 2. Save review details in clothes detail table
        await insert_outfit_review_detail(
            wardrobe_id=job["wardrobe_id"],
            user_id=job["user_id"],
            review=review_data
        )

        # 3. Update registry
        job_id = get_job_id_by_job(job)
        update_registry(job_id, "review_status", "finished")

        # 4. Update Supabase wardrobe entry
        supabase = await get_supabase_client()
        await supabase.from_(REVIEW_TABLE).update({
            "outfit_review": review_data["review"],
            "style_rating": review_data["style_rating"],
            "color_match_rating": review_data["color_match_rating"],
            "piece_match_rating": review_data["piece_match_rating"],
            "overall_rating": review_data["overall_rating"],
            "review_status": "finished"
        }).eq("image_url", job["image_url"]).execute()

        return review_data

    except Exception as e:
        print(f"[Outfit Review Service] Error: {e}")
        return "Error generating review"
