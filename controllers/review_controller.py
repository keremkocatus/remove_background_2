import asyncio
from fastapi import APIRouter, File, Form, UploadFile, HTTPException
import routes
from services.review_services.review_service import process_outfit_review_for_job
from services.supabase_services.upload_service import upload_image_review
from utils.review_registery import get_review_job_status, register_review_job

review_router = APIRouter()

@review_router.post(routes.REVIEW_OUTFIT)
async def review_outfit_process(
    user_id: str = Form(...),
    image: UploadFile = File(...),
    roast_level: str = Form(...)
):
    try:
        # --- Upload & job kaydı ---
        public_url, bucket_id = await upload_image_review(user_id, image)
        job_id = register_review_job(public_url, user_id, int(roast_level), bucket_id)
        
        loop = asyncio.get_running_loop()
        loop.create_task(process_outfit_review_for_job(job_id))

        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in review process: {e}"
        )


@review_router.get(routes.REVIEW_JOB_STATUS)
async def fetch_job_status(job_id: str):
    try:
        return await get_review_job_status(job_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching job status for {job_id}: {e}"
        )