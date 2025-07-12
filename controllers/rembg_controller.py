from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Request
import asyncio

from services.caption_services.caption_service import get_caption_for_image
from services.replicate_services.rembg_service import get_job_status, handle_fast_webhook, handle_quality_webhook, trigger_prediction
from services.replicate_services.rembg_service import register_rembg_job
from services.supabase_services.insert_service import insert_job_record
from services.supabase_services.upload_service import upload_image

rembg_router = APIRouter()

@rembg_router.post("/wardrobe/remove-background")
async def wardrobe_background_removal(user_id: str = Form(...), clothe_image: UploadFile = File(...),
                            is_fast: bool = Form(...), category: str = Form(...), is_long_top: bool = Form(False)):
    try:
        public_url, bucket_id = await upload_image(user_id, clothe_image, category)
        job_id = register_rembg_job(public_url, user_id, bucket_id, category, is_long_top)
        await insert_job_record(job_id, public_url, user_id, category, is_long_top)

        loop = asyncio.get_running_loop()
        loop.create_task(get_caption_for_image(public_url))
        loop.create_task(trigger_prediction(job_id, is_fast))

        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in wardrobe background removal: {e}"
        )

@rembg_router.get("/job-status/{job_id}")
async def fetch_job_status(job_id: str):
    try:
        return await get_job_status(job_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching job status for {job_id}: {e}"
        )

@rembg_router.post("/webhook/replicate/fast")
async def replicate_fast_webhook(request: Request):
    try:
        payload = await request.json()
        await handle_fast_webhook(payload)
        
        return {"status": "Webhook received successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing fast webhook: {e}"
        )

@rembg_router.post("/webhook/replicate/quality")
async def replicate_quality_webhook(request: Request):
    try:
        payload = await request.json()
        await handle_quality_webhook(payload)
        
        return {"status": "Webhook received successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing quality webhook: {e}"
        )
