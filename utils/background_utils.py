import uuid
from services.replicate_service import remove_background_replicate
from services.supabase_wardrobe_service import upload_bg_removed

def backgroundtasks_rmbg(user_id: uuid.UUID, bucket_uuid: uuid.UUID, job_id: uuid.UUID, 
                         public_url: str, category: str, islongtop: bool):
    
    bg_removed_image = remove_background_replicate(public_url, category, islongtop)
    resp = upload_bg_removed(user_id,bucket_uuid,job_id,bg_removed_image,category)