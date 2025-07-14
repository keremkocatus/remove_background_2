from services.supabase_services.client_service import get_supabase_client
import os
from dotenv import load_dotenv

load_dotenv()
bucket_name = os.getenv("WARDROBE_BUCKET_NAME")

async def mark_job_failed(job_id: str, bucket_name: str = bucket_name) -> None:
    supabase = await get_supabase_client()
    await supabase.from_(bucket_name).update({"enhance_status": "failed"}).eq(
        "job_id", job_id
    ).execute()