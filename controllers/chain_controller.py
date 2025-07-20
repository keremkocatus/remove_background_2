import asyncio
from fastapi import APIRouter, File, Form, UploadFile, HTTPException

from services.supabase_services.upload_service import upload_image
from services.supabase_services.insert_service import insert_job_record
from utils.registery import get_job_status, register_job

from services.caption_services.caption_service import get_caption_for_image
from services.replicate_services.rembg_service import (
    get_job_by_id as get_rembg_job,
    trigger_rembg,
)
from services.replicate_services.enhance_service import (
    trigger_prediction as trigger_enhance,
)

chain_router = APIRouter()

async def _chain_remove_background(job_id: str, is_fast: bool):
    """
    Zincirleme fonksiyon: önce caption, sonra background removal.
    """
    try:
        job = get_rembg_job(job_id)
        loop = asyncio.get_running_loop()

        # 1) Caption
        loop.create_task(get_caption_for_image(job))
        # 2) Background removal
        loop.create_task(trigger_rembg(job_id, is_fast))
    except Exception as e:
        print(f"[chain_remove_background] Error: {e}")


@chain_router.post("/chain/process")
async def chain_process(
    user_id: str = Form(...),
    clothe_image: UploadFile = File(...),
    category: str = Form(...),
    is_long_top: bool = Form(False),
    is_enhance: bool = Form(False),
    is_fast: bool = Form(True),
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
            loop.create_task(_chain_remove_background(job_id, is_fast))

        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in chain process: {e}"
        )

@chain_router.get("/chain/job-status/{job_id}/{is_enhance}")
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