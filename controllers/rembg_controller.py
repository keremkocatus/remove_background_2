from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Request
from services.supabase_wardrobe_service import upload_original_image, insert_job_record, get_caption_of_image
from services.replicate_rembg_service import (register_job,trigger_prediction,get_job_status,
                                              handle_quality_webhook,handle_fast_webhook,)
import asyncio

router = APIRouter()

@router.post("/wardrobe/remove-background")
async def wardrobe_background_removal(user_id: str = Form(...), clothe_image: UploadFile = File(...),
                            is_fast: bool = Form(...), category: str = Form(...), is_long_top: bool = Form(False)):
    try:
        print(is_fast)
        public_url, bucket_id = await upload_original_image(user_id, clothe_image, category)
        job_id = register_job(public_url, user_id, bucket_id, category, is_long_top)
        await insert_job_record(job_id, public_url, user_id, category, is_long_top)

        loop = asyncio.get_running_loop()
        loop.create_task(trigger_prediction(job_id, is_fast))

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

@router.get("/wardrobe/caption")
async def generate_caption(image_url: str):
    """
    Generate or retrieve a caption for an image using ChatGPT
    
    Args:
        image_url: The URL of the image to get caption for
    
    Returns:
        Generated caption
    """
    try:
        caption = await get_caption_of_image(image_url)
        return {
            "image_url": image_url,
            "caption": caption
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating caption: {e}"
        )

@router.post("/webhook/replicate/fast")
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
