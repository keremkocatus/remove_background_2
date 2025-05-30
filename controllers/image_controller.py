from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks
from services.rembg_service import remove_background_rembg
from services.supabase_wardrobe_service import upload_supabase, insert_supabase
from utils.background_utils import backgroundtasks_rmbg
import uuid

router = APIRouter()

# post clothe background remove
@router.post("/wardrobe-remove-background")
async def clothe_rembg(user_id: uuid.UUID, clothe_image: UploadFile, category: str, 
                       islongtop: bool, background_tasks: BackgroundTasks):
    
    try:
        public_url, bucket_uuid = await upload_supabase(user_id, clothe_image, category)
        job_id = await insert_supabase(public_url,user_id,category,islongtop)
        
        background_tasks.add_task(backgroundtasks_rmbg, user_id,bucket_uuid,job_id,public_url,category,islongtop)
        
        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process-image")
async def process_image(photo: UploadFile = File(...),clothing: UploadFile = File(...)):
    try:
        return await remove_background_rembg(photo, clothing)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))