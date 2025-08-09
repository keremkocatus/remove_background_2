from services.supabase_services.client_service import get_supabase_client
from utils.edit_registery import update_edit_registry
from utils.wardrobe_registery import update_registry
from core import config

bucket_name = config.WARDROBE_BUCKET_NAME
error_log_table = config.ERROR_LOG_TABLE
EDIT_TABLE_NAME = config.EDIT_TABLE_NAME

async def mark_job_failed(job_id: str, bucket_name: str = bucket_name) -> None:
    supabase = await get_supabase_client()

    update_registry(job_id, "enhance_status", "failed")
    update_registry(job_id, "rembg_status", "failed")
    update_registry(job_id, "caption_status", "failed")

    await supabase.from_(bucket_name).update({
        "enhance_status": "failed",
        "rembg_status": "failed",
        "caption_status": "failed"
    }).eq("job_id", job_id).execute()


async def mark_edit_job_failed(job_id: str, bucket_name: str = EDIT_TABLE_NAME) -> None:
    supabase = await get_supabase_client()

    update_edit_registry(job_id, "status", "failed")

    await supabase.from_(bucket_name).update({
        "enhance_status": "failed",
        "rembg_status": "failed",
        "caption_status": "failed"
    }).eq("job_id", job_id).execute()
