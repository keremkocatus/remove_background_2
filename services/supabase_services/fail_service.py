from services.supabase_services.client_service import get_supabase_client
from utils.registery import get_job_by_id, update_registry
import os
from dotenv import load_dotenv

load_dotenv()
bucket_name = os.getenv("WARDROBE_BUCKET_NAME")
error_log_table = os.getenv("ERROR_LOG_TABLE")

async def mark_job_failed(job_id: str, bucket_name: str = bucket_name) -> None:
    supabase = await get_supabase_client()

    update_registry(job_id, "enhance_status", "failed")
    update_registry(job_id, "rembg_status", "failed")
    update_registry(job_id, "caption_status", "failed")

    await supabase.from_(bucket_name).update({
        "enhance_status": "failed",
        "rembg_status": "failed",
        "caption_status": "failed"}).eq(
        "job_id", job_id
    ).execute()

async def upload_error_log(job_id: str, failed_tasks: list):
    supabase = await get_supabase_client()
    job = get_job_by_id(job_id)

    await supabase.from_(error_log_table).insert({
        "user_id": job["user_id"],
        "job_id": job_id,
        "image_url": job["image_url"],
        "failed_tasks": failed_tasks,
    }).execute()