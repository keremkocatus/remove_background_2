from services.supabase_services.client_service import get_supabase_client
from core import config

BUCKET_NAME = config.WARDROBE_BUCKET_NAME
CLOTHE_DETAIL_TABLE = config.CLOTHES_DETAIL_TABLE

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
    
async def check_clothe_detail(wardrobe_id: str):
    try:
        supabase = await get_supabase_client()
        
        resp = await supabase.from_(CLOTHE_DETAIL_TABLE).select("*")\
            .eq("wardrobe_item_id", wardrobe_id).execute()
        
        if not resp.count == 0:
            return True
        else:
            return False
        
    except Exception as e:
        raise RuntimeError(f"Supabase clothe detai error: {e}")
