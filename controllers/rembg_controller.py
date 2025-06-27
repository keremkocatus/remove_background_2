from fastapi import APIRouter, File, Form ,UploadFile, HTTPException
from services.supabase_wardrobe_service import upload_supabase, insert_supabase
from services.replicate_rembg_service import create_job, start_replicate_prediction, check_job_status
import asyncio

router = APIRouter()

# post wardrobe clothe background remove
@router.post("/wardrobe-remove-background")
async def remove_clothing_background(user_id: str = Form(...), clothe_image: UploadFile = File(...), 
                       category: str = Form(...), is_long_top: bool = Form(False)):
    try:
        public_url, bucket_uuid = await upload_supabase(user_id, clothe_image, category)
        job_id = create_job(public_url, user_id, bucket_uuid, category, is_long_top)
        resp = await insert_supabase(job_id, public_url, user_id, category, is_long_top)
        
        loop = asyncio.get_running_loop()
        loop.create_task(start_replicate_prediction(job_id))

        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"wardrobe-background-remove: {str(e)}")

# post wardrobe job_status 
@router.post("/job-status/{job_id}")
async def job_status(job_id: str):
    try:
        return await check_job_status(job_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"job-status/{job_id}: {e}")
