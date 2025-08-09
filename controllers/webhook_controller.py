from fastapi import APIRouter, HTTPException, Request
from controllers.chain_controller import chain_remove_background
from services.replicate_services.image_edit_service import handle_edit_webhook
from services.replicate_services.enhance_service import handle_enhance_webhook
from services.replicate_services.late_enhance_service import handle_late_enhance_webhook, late_chain_remove_background
from services.replicate_services.rembg_service import handle_fast_webhook
import asyncio
import core.routes as routes
from services.supabase_services.fail_service import mark_job_failed


webhook_router = APIRouter()

@webhook_router.post(routes.WEBHOOK_FAST_REMBG)
async def replicate_fast_webhook(request: Request):
    try:
        payload = await request.json()
        status = payload.get("status")

        if status == "succeeded":
            job_id = await handle_fast_webhook(payload)
            
            return {"status": "Webhook rembg received successfully"}
        else:
            await mark_job_failed(job_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing fast webhook: {e}"
        )
    

@webhook_router.post(routes.WEBHOOK_ENHANCE)
async def replicate_enhance_webhook(request: Request):
    """
    Webhook endpoint for replicate enhance predictions (e.g. once 'succeeded').
    """
    try:
        payload = await request.json()
        status = payload.get("status")

        if status == "succeeded":
            job_id, job = await handle_enhance_webhook(payload)

            loop = asyncio.get_running_loop()
            loop.create_task(chain_remove_background(job_id))

            return {"status": "Enhance webhook received successfully, and rembg started"}
        else:
            await mark_job_failed(job_id)

            return {"status": "failed"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing enhance webhook: {e}"
        )
        
@webhook_router.post(routes.WEBHOOK_LATE_ENHANCE)
async def replicate_enhance_webhook(request: Request):
    """
    Webhook endpoint for replicate enhance predictions (e.g. once 'succeeded').
    """
    try:
        payload = await request.json()
        status = payload.get("status")

        if status == "succeeded":
            job_id, job = await handle_late_enhance_webhook(payload)

            loop = asyncio.get_running_loop()
            loop.create_task(late_chain_remove_background(job_id))

            return {"status": "Enhance webhook received successfully, and rembg started"}
        else:
            await mark_job_failed(job_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing enhance webhook: {e}"
        )
        
@webhook_router.post(routes.WEBHOOK_IMAGE_EDIT)
async def replicate_edit_webhook(request: Request):
    """
    Webhook endpoint for replicate edit predictions (e.g. once 'succeeded').
    """
    try:
        payload = await request.json()
        status = payload.get("status")

        if status == "succeeded":
            job_id, job = await handle_edit_webhook(payload)

            return {"status": "Edit webhook received successfully"}
        else:
            await mark_job_failed(job_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing edit webhook: {e}")