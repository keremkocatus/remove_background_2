import asyncio
from fastapi import APIRouter, Form, HTTPException, Request
from controllers.chain_controller import _chain_remove_background
from services.replicate_services.late_enhance_service import (
    get_job_status,
    trigger_prediction as trigger_enhance,
    handle_enhance_webhook, 
)

late_enhance_router = APIRouter()

@late_enhance_router.post("/wardrobe/late/enhance-image")
async def enhance_image(
    user_id: str = Form(...), image_url: str = Form(...)
):
    try:
        output = await trigger_enhance(image_url)

        return {"status": "200 OK"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in enhance image: {e}"
        )

@late_enhance_router.get("/job-status/{job_id}")
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

@late_enhance_router.post("/webhook/replicate-enhance")
async def replicate_enhance_webhook(request: Request):
    """
    Webhook endpoint for replicate enhance predictions (e.g. once 'succeeded').
    """
    try:
        payload = await request.json()
        job_id, job = await handle_enhance_webhook(payload)

        asyncio.get_running_loop().create_task(_chain_remove_background(job_id, is_fast=True))

        return {"status": "Enhance webhook received successfully, and remb started"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing enhance webhook: {e}"
        )
