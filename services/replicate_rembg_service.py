import os
import uuid
import replicate
import asyncio
from fastapi import HTTPException
from dotenv import load_dotenv
from services.supabase_wardrobe_service import mark_job_failed
from utils.webhook_utils import get_job_id_by_prediction
from utils.prompt_utils import get_mask_prompts
from utils.background_utils import start_low_quality_background_process, start_quality_background_process

load_dotenv()
replicate_api_token = os.getenv("REPLICATE_API_TOKEN")
replicate_client = replicate.Client(api_token=replicate_api_token)

QUALITY_MODEL_ID = "ee871c19efb1941f55f66a3d7d960428c8a5afcb77449547fe8e5a3ab9ebc21c"
LOW_QUALITY_MODEL_ID = "a029dff38972b5fda4ec5d75d7d1cd25aeff621d2cf4946a41055d7db66b80bc"
REPLICATE_WEBHOOK_URL = "https://5f6f-88-232-8-144.ngrok-free.app"

# In-memory registry for pending jobs
JOB_REGISTRY: dict[str, dict] = {}

# Register a new background-removal job and return its identifier
def register_job(image_url: str, user_id: str, bucket_id: str, category: str, is_long_top: bool = False) -> str:
    job_id = str(uuid.uuid4())
    JOB_REGISTRY[job_id] = {
        "status": "processing",
        "prediction_id": None,
        "user_id": user_id,
        "bucket_id": bucket_id,
        "image_url": image_url,
        "category": category,
        "is_long_top": is_long_top,
        "result_url": None,
    }
    return job_id

# Submit an asynchronous prediction request to Replicate
async def trigger_prediction(job_id: str, low_quality: bool):
    job = JOB_REGISTRY[job_id]
    mask_prompt, negative_mask_prompt = get_mask_prompts(job["category"], job["is_long_top"])

    if low_quality:
        prediction_input = {
            "image": job["image_url"],
            "format": "png",
            "reverse": False,
            "threshold": -20,
            "background_type": "rgba",
        }
        model_id = LOW_QUALITY_MODEL_ID
        webhook_url = f"{REPLICATE_WEBHOOK_URL}/webhook/replicate/low-quality"
    else:
        prediction_input = {
            "image": job["image_url"],
            "mask_prompt": mask_prompt,
            "adjustment_factor": -20,
            "negative_mask_prompt": negative_mask_prompt,
        }
        model_id = QUALITY_MODEL_ID
        webhook_url = f"{REPLICATE_WEBHOOK_URL}/webhook/replicate/quality"

    prediction = await replicate_client.predictions.async_create(
        version=model_id,
        input=prediction_input,
        webhook=webhook_url,
        webhook_events_filter=["completed"],
    )
    JOB_REGISTRY[job_id]["prediction_id"] = prediction.id

# Handle webhook event for high-quality prediction completion
async def handle_quality_webhook(payload: dict):
    job_id = None
    try:
        prediction_id = payload["id"]
        job_id, job = get_job_id_by_prediction(prediction_id, JOB_REGISTRY)
        
        loop = asyncio.get_running_loop()
        loop.create_task(start_quality_background_process(payload, job_id, job))
    except Exception as e:
        if job_id:
            await mark_job_failed(job_id)
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {e}")

# Handle webhook event for low-quality prediction completion
async def handle_low_quality_webhook(payload: dict):
    job_id = None
    try:
        prediction_id = payload["id"]
        job_id, job = get_job_id_by_prediction(prediction_id, JOB_REGISTRY)
        
        loop = asyncio.get_running_loop()
        loop.create_task(start_low_quality_background_process(payload, job_id, job))
    except Exception as e:
        if job_id:
            await mark_job_failed(job_id)
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {e}")

# Retrieve current status of a registered job
async def get_job_status(job_id: str) -> dict:
    job = JOB_REGISTRY.get(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job does not exist")
    
    if job["status"] == "processing":
        return {"status": "processing"}
    
    if job["status"] == "finished":
        return {"status": "finished", "result_url": job["result_url"]}
    raise HTTPException(status_code=500, detail="Unknown job status")
