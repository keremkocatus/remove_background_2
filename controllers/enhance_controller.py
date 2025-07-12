import asyncio
from fastapi import APIRouter, Form, HTTPException, Request
from services.replicate_services.enhance_service import (
    get_job_status,
    trigger_prediction,
    handle_enhance_webhook, 
)

enhance_router = APIRouter()

@enhance_router.post("/wardrobe/enhance-image")
async def enhance_image(
    job_id: str = Form(...),
):
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(trigger_prediction(job_id))

        return {"status": "200 OK"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in enhance image: {e}"
        )

@enhance_router.get("/job-status/{job_id}")
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

@enhance_router.post("/webhook/replicate-enhance")
async def replicate_enhance_webhook(request: Request):
    """
    Webhook endpoint for replicate enhance predictions (e.g. once 'succeeded').
    """
    try:
        payload = await request.json()
        await handle_enhance_webhook(payload)
        return {"status": "Enhance webhook received successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing enhance webhook: {e}"
        )
