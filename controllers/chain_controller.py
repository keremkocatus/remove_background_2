import asyncio
from fastapi import APIRouter, File, Form, UploadFile, HTTPException

from services.chain_services.chain_service import chain_remove_background
from services.supabase_services.upload_service import upload_image
from services.supabase_services.insert_service import insert_job_record
from services.replicate_services.enhance_service import trigger_prediction as trigger_enhance

from utils.wardrobe_registery import get_job_status, register_job
import core.routes as routes

chain_router = APIRouter()

@chain_router.post(routes.CHAIN_PROCESS)
async def chain_process(
    user_id: str = Form(...),
    clothe_image: UploadFile = File(...),
    category: str = Form(...),
    is_long_top: bool = Form(False),
    is_enhance: bool = Form(False),
):
    """
    1) Supabase'a upload & job kaydı
    2) Eğer is_enhance:
         - önce enhance tetiklenir
         - tamamlandıktan sonra rembg başlatılır
       Aksi halde direkt rembg.
    """
    try:
        # --- Upload & job kaydı ---
        public_url, bucket_id = await upload_image(user_id, clothe_image, category)
        job_id = register_job(public_url, user_id, bucket_id, category, is_long_top)
        await insert_job_record(job_id)

        loop = asyncio.get_running_loop()
        if is_enhance:
            loop.create_task(trigger_enhance(job_id))
        else:
            # Direkt arkaplanda rembg
            loop.create_task(chain_remove_background(job_id))

        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in chain process: {e}"
        )

@chain_router.get(routes.CHAIN_JOB_STATUS)
async def fetch_job_status(job_id: str, is_enhance: bool):
    try:
        return get_job_status(job_id, is_enhance)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching job status for {job_id}: {e}"
        )