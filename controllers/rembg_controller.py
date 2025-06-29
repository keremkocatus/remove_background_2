from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Request
from services.supabase_wardrobe_service import upload_original_image, insert_job_record
from services.replicate_rembg_service import (register_job,trigger_prediction,get_job_status,
                                              handle_quality_webhook,handle_low_quality_webhook,)
import asyncio

router = APIRouter()

@router.post("/wardrobe/remove-background")
async def wardrobe_background_removal(user_id: str = Form(...), clothe_image: UploadFile = File(...),
                            is_low_quality: bool = Form(...), category: str = Form(...), is_long_top: bool = Form(False)):
    try:
        public_url, bucket_id = await upload_original_image(user_id, clothe_image, category)
        job_id = register_job(public_url, user_id, bucket_id, category, is_long_top)
        await insert_job_record(job_id, public_url, user_id, category, is_long_top)

        loop = asyncio.get_running_loop()
        loop.create_task(trigger_prediction(job_id, is_low_quality))

        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in wardrobe background removal: {e}"
        )

@router.get("/job-status/{job_id}")
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

@router.post("/webhook/replicate/low-quality")
async def replicate_low_quality_webhook(request: Request):
    try:
        payload = await request.json()
        await handle_low_quality_webhook(payload)
        
        return {"status": "Webhook received successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing low-quality webhook: {e}"
        )

@router.post("/webhook/replicate/quality")
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
