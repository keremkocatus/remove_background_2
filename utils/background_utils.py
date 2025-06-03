from services.replicate_wardrobe_service import remove_background_replicate
from services.supabase_wardrobe_service import upload_bg_removed

async def backgroundtasks_rmbg(user_id: str, bucket_uuid: str, job_id: str, 
                         public_url: str, category: str, is_long_top: bool):
    try:
        bg_removed_image = await remove_background_replicate(public_url, category, is_long_top)
        resp = await upload_bg_removed(user_id, bucket_uuid, job_id, bg_removed_image, category)
    except Exception as e:
        print(f"Error in backgroundtasks_rmbg: {e}")
