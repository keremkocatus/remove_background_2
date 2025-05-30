from services.replicate_service import remove_background_replicate
from services.supabase_wardrobe_service import upload_bg_removed

async def backgroundtasks_rmbg(user_id: str, bucket_uuid: str, job_id: str, 
                         public_url: str, category: str, islongtop: bool):
    
    bg_removed_image = await remove_background_replicate(public_url, category, islongtop)
    resp = await upload_bg_removed(user_id,bucket_uuid,job_id,bg_removed_image,category)