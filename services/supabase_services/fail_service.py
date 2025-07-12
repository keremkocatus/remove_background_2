from services.supabase_services.client_service import get_supabase_client

async def mark_job_failed(job_id: str, bucket_name: str) -> None:
    supabase = await get_supabase_client()
    await supabase.from_(bucket_name).update({"status": "failed"}).eq(
        "job_id", job_id
    ).execute()