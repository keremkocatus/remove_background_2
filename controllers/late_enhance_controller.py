import asyncio
from fastapi import APIRouter, Form, HTTPException, Request
from controllers.chain_controller import chain_remove_background
from services.replicate_services.enhance_service import (
    trigger_prediction as trigger_enhance)

from route_loader import load_routes
from services.supabase_services.fetch_service import fetch_job_record
from services.supabase_services.insert_service import update_job_record
from utils.registery import insert_late_enhance_record

routes = load_routes()

late_enhance_router = APIRouter()

@late_enhance_router.post(routes.late_enhance)
async def late_enhance_image(
    user_id: str = Form(...), 
    image_url: str = Form(...),
    is_enhance: bool = Form(True),
    #wardrobe_id: str = Form(...)
):
    try:
        record = await fetch_job_record(user_id, image_url)
        job_id = insert_late_enhance_record(record)
        await update_job_record(job_id)
        
        loop = asyncio.get_running_loop()
        if is_enhance:
            loop.create_task(trigger_enhance(job_id))
        else:
            # Direkt arkaplanda rembg
            loop.create_task(chain_remove_background(job_id))
        
        return {"status": job_id}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in enhance image: {e}"
        )
