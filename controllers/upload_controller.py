from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Request

from services.supabase_services.insert_service import insert_job_record
from services.supabase_services.upload_service import upload_image
from utils.registery import register_job

upload_router = APIRouter()

@upload_router.post("/supabase/upload/image")
async def wardrobe_background_removal(user_id: str = Form(...), clothe_image: UploadFile = File(...),
                            category: str = Form(...), is_long_top: bool = Form(False)):
    try:
        public_url, bucket_id = await upload_image(user_id, clothe_image, category)
        job_id = register_job(public_url, user_id, bucket_id, category, is_long_top)
        await insert_job_record(job_id, public_url, user_id, category, is_long_top)

        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in wardrobe background removal: {e}"
        )