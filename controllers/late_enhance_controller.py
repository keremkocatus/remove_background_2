import asyncio
from fastapi import APIRouter, Form, HTTPException
from controllers.chain_controller import chain_remove_background
from services.caption_services.caption_service import get_caption_for_image
from services.replicate_services.late_enhance_service import trigger_late_enhance
from services.supabase_services.fetch_service import check_clothe_detail, fetch_job_record
from services.supabase_services.insert_service import update_job_record
from utils.registery import get_job_by_id, get_job_status, insert_late_enhance_record
import routes


late_enhance_router = APIRouter()

@late_enhance_router.post(routes.LATE_ENHANCE)
async def late_enhance_image(
    user_id: str = Form(...), 
    image_url: str = Form(...),
    is_enhance: bool = Form(True),
    wardrobe_id: str = Form(...)
):
    """
    late enhance, if there is clothe detail caption service will not work
    late enhance, if there is clothe detail caption service will work
    late, enhance, will fetch record wardrobe table and it will update
    """
    try:
        record = await fetch_job_record(user_id, image_url)
        job_id = insert_late_enhance_record(record)
        await update_job_record(job_id)
        
        is_caption = await check_clothe_detail(wardrobe_id)
        
        loop = asyncio.get_running_loop()
        if is_enhance and is_caption:
            job = get_job_by_id(job_id)
            
            loop.create_task(get_caption_for_image(job))
            loop.create_task(trigger_late_enhance(job_id))
        elif is_enhance and is_caption:
            loop.create_task(trigger_late_enhance(job_id))
        else:
            # arkaplanda rembg
            loop.create_task(chain_remove_background(job_id))
        
        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in enhance image: {e}"
        )

# send always true for is_enhance
@late_enhance_router.get(routes.LATE_ENHANCE_JOB_STATUS)
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