import asyncio
import os
from supabase import AsyncClient
from dotenv import load_dotenv

from services.openai_services.generate_review import generate_outfit_review
from services.supabase_services.insert_service import insert_review_job_record
from utils.review_registery import update_review_registry, get_review_job_by_id

load_dotenv()
REVIEW_TABLE = os.getenv("REVIEW_TABLE")

async def get_supabase_client() -> AsyncClient:
    from services.supabase_services.client_service import get_supabase_client as _get
    return await _get()

async def process_outfit_review_for_job(job_id: str) -> dict | str:
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
        # 0. Get job by job_id
        job = get_review_job_by_id(job_id)

        # 1. Generate outfit review using OpenAI
        review_data = await generate_outfit_review(job["image_url"], job["roast_level"], job["job_id"])

        # 2. Save review details in table
        await insert_review_job_record(
            job=job,
            result=review_data
        )

        # 3. Update registry
        update_review_registry(job_id, "result", review_data)
        update_review_registry(job_id, "review_status", "finished")

    except Exception as e:
        print(f"[Outfit Review Service] Error: {e}")
        return "Error generating review"
