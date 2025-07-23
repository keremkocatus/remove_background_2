from fastapi import APIRouter, HTTPException, Request
from controllers.chain_controller import chain_remove_background
from services.replicate_services.enhance_service import handle_enhance_webhook
from services.replicate_services.rembg_service import handle_fast_webhook
import asyncio
from route_loader import load_routes


routes = load_routes()

webhook_router = APIRouter()

@webhook_router.post(routes.webhook.fast_rembg)
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
    

@webhook_router.post(routes.webhook.enhance)
async def replicate_enhance_webhook(request: Request):
    """
    Webhook endpoint for replicate enhance predictions (e.g. once 'succeeded').
    """
    try:
        payload = await request.json()
        job_id, job = await handle_enhance_webhook(payload)

        loop = asyncio.get_running_loop()
        loop.create_task(chain_remove_background(job_id))

        return {"status": "Enhance webhook received successfully, and remb started"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing enhance webhook: {e}"
        )