from services.supabase_services.client_service import get_supabase_client
import os

BUCKET_NAME = os.getenv("WARDROBE_BUCKET_NAME")

async def fetch_job_record(user_id: str, image_url: str) -> dict:
    try:
        supabase = await get_supabase_client()

        response = await supabase.from_(BUCKET_NAME).select("*") \
            .eq("user_id", user_id) \
            .eq("image_url", image_url) \
            .single() \
            .execute()

        return response.data

    except Exception as e:
        raise RuntimeError(f"Supabase fetch error: {e}")
    
