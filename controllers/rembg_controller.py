from fastapi import APIRouter, Form, HTTPException, Request
import asyncio

from services.caption_services.caption_service import get_caption_for_image
from services.replicate_services.rembg_service import get_job_status, get_job_by_id ,handle_fast_webhook, handle_quality_webhook, trigger_prediction

rembg_router = APIRouter()

@rembg_router.post("/wardrobe/remove-background")
async def wardrobe_background_removal(job_id: str = Form(...), is_fast: bool = Form(True)):
    try:
        job = get_job_by_id(job_id)

        loop = asyncio.get_running_loop()
        loop.create_task(get_caption_for_image(job["image_url"]))
        loop.create_task(trigger_prediction(job_id, is_fast))

        return {"status": "200 OK"}
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
