from fastapi import APIRouter, File, Form ,UploadFile, HTTPException
from services.rembg_service import segment_human_from_background
from services.supabase_wardrobe_service import upload_supabase, insert_supabase
from utils.background_utils import backgroundtasks_rmbg
import asyncio

router = APIRouter()

# post wardrobe clothe background remove
@router.post("/wardrobe-remove-background")
async def remove_clothing_background(user_id: str = Form(...), clothe_image: UploadFile = File(...), 
                       category: str = Form(...), is_long_top: bool = Form(...)):
    try:
        public_url, bucket_uuid = await upload_supabase(user_id, clothe_image, category)
        job_id = await insert_supabase(public_url,user_id,category,is_long_top)
        
        loop = asyncio.get_running_loop()
        loop.create_task(backgroundtasks_rmbg(user_id,bucket_uuid,job_id,public_url,category,is_long_top))
        print("test")
        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"wardrobe-background-remove: {str(e)}")

#post replicate human segmentation
@router.post("/replicate-human-segmentation")
async def replicate_human_segmentation():
    pass

# post u2net human segmentation
@router.post("/u2net-human-segmentation")
async def segment_human_u2net(photo: UploadFile = File(...)):
    try:
        return await segment_human_from_background(photo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"u2net-human-segmentation: {str(e)}")