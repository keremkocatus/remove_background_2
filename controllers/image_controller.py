from fastapi import APIRouter, File, Form ,UploadFile, HTTPException
from services.rembg_service import remove_background_rembg
from services.supabase_wardrobe_service import upload_supabase, insert_supabase
from utils.background_utils import backgroundtasks_rmbg
import asyncio

router = APIRouter()

# post clothe background remove
@router.post("/wardrobe-remove-background")
async def clothe_rembg(user_id: str = Form(...), clothe_image: UploadFile = Form(...), 
                       category: str = Form(...), is_long_top: bool = Form(...)):
    try:
        public_url, bucket_uuid = await upload_supabase(user_id, clothe_image, category)
        job_id = await insert_supabase(public_url,user_id,category,is_long_top)
        
        asyncio.create_task(backgroundtasks_rmbg(user_id,bucket_uuid,job_id,public_url,category,is_long_top))
        
        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"wardrobe-background-remove: {str(e)}")

@router.post("/process-image")
async def process_image(photo: UploadFile = File(...),clothing: UploadFile = File(...)):
    try:
        return await remove_background_rembg(photo, clothing)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"process-image: {str(e)}")