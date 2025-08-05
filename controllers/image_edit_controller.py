import asyncio
from fastapi import APIRouter, File, Form, UploadFile, HTTPException
import routes
from services.supabase_services.insert_service import insert_edit_job_record
from services.supabase_services.upload_service import upload_image_edit
from utils.edit_registery import get_edit_job_status, register_edit_job
from services.replicate_services.image_edit_service import trigger_edit_prediction

image_edit_router = APIRouter()

@image_edit_router.post(routes.IMAGE_EDIT)
async def image_edit_process(
    user_id: str = Form(...),
    image: UploadFile = File(...),
    prompt: str = Form(...)
):
    try:
        # --- Upload & job kaydı ---
        public_url, bucket_id = await upload_image_edit(user_id, image)
        job_id = register_edit_job(public_url, user_id, prompt, bucket_id)
        await insert_edit_job_record(job_id)

        loop = asyncio.get_running_loop()
        loop.create_task(trigger_edit_prediction(job_id))

        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in chain process: {e}"
        )


@image_edit_router.get(routes.EDIT_JOB_STATUS)
async def fetch_job_status(job_id: str):
    try:
        return await get_edit_job_status(job_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching job status for {job_id}: {e}"
        )