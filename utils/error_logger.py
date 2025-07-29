from services.supabase_services.client_service import get_supabase_client
import os

error_log_table = os.getenv("ERROR_LOG_TABLE")

async def upload_error_log(user_id: str, image_url: str, job_id: str, failed_tasks: list = []):
    supabase = await get_supabase_client()

    await supabase.from_(error_log_table).insert({
        "user_id": user_id,
        "job_id": job_id,
        "image_url": image_url,
        "failed_tasks": failed_tasks,
    }).execute()
