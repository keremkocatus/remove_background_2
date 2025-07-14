from fastapi import APIRouter, File, Form, UploadFile, HTTPException

from services.supabase_services.insert_service import insert_job_record
from services.supabase_services.upload_service import upload_image
from utils.registery import register_job

upload_router = APIRouter()

@upload_router.post("/supabase/upload/image")
async def upload_to_supabase(user_id: str = Form(...), clothe_image: UploadFile = File(...),
                            category: str = Form(...), is_long_top: bool = Form(False),
                            is_enhance: bool = Form(False)):
    try:
        public_url, bucket_id = await upload_image(user_id, clothe_image, category)
        job_id = register_job(public_url, user_id, bucket_id, category, is_long_top)
        await insert_job_record(job_id)

        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in upload image: {e}"
        )