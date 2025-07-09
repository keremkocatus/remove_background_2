import asyncio
import os
import uuid
import replicate
from fastapi import HTTPException
from dotenv import load_dotenv
from utils.background_utils import start_enhance_background_process

from services.supabase_wardrobe_service import mark_job_failed
from utils.webhook_utils import get_job_id_by_prediction

load_dotenv()
replicate_api_token = os.getenv("REPLICATE_API_TOKEN")
replicate_client = replicate.Client(api_token=replicate_api_token)

MODEL_ID = os.getenv("ENHANCE_MODEL_ID")
ENHANCE_WEBHOOK_URL = f"{os.getenv("REPLICATE_WEBHOOK_URL")}/webhook/replicate-enhance"

# In-memory registry for pending jobs
ENHANCE_REGISTRY: dict[str, dict] = {}

# Register a new background-removal job and return its identifier
def register_job(image_url: str, user_id: str, bucket_id: str) -> str:
    job_id = str(uuid.uuid4())

    ENHANCE_REGISTRY[job_id] = {
        "status": "processing",
        "prediction_id": None,
        "user_id": user_id,
        "bucket_id": bucket_id,
        "image_url": image_url,
        "result_url": None,
    }
    return job_id

async def trigger_prediction(job_id: str):
    job = ENHANCE_REGISTRY[job_id]

    prediction_input = {
        "prompt": "Please extract the clothing item from the given real-world image and convert it into a clean, flat-lay digital version. Ensure the shape, proportions, and color of the garment are preserved accurately in the transformation. Remove the background, accessories, and shadows for a clear, studio-style presentation. The final output should resemble a catalog image with only the clothing item visible on a plain white or transparent background.",
        "input_image": job["image_url"],
        "output_format": "jpg"
    }

    prediction = await replicate_client.predictions.async_create(
        version=MODEL_ID,
        input=prediction_input,
        webhook=ENHANCE_WEBHOOK_URL,
        webhook_events_filter=["completed"],
    )

    ENHANCE_REGISTRY[job_id]["prediction_id"] = prediction.id

# Handle webhook event for fast prediction completion
async def handle_fast_webhook(payload: dict):
    job_id = None
    try:
        prediction_id = payload["id"]
        job_id, job = get_job_id_by_prediction(prediction_id, ENHANCE_REGISTRY)
        
        loop = asyncio.get_running_loop()
        loop.create_task(start_enhance_background_process(payload, job_id, job))
    except Exception as e:
        if job_id:
            await mark_job_failed(job_id)
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {e}")

# Retrieve current status of a registered job
async def get_job_status(job_id: str) -> dict:
    job = ENHANCE_REGISTRY.get(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job does not exist")
    
    if job["status"] == "processing":
        return {"status": "processing"}
    
    if job["status"] == "finished":
        result_url = job["result_url"]
        del ENHANCE_REGISTRY[job_id]

        return {"status": "finished", "result_url": result_url}
    raise HTTPException(status_code=500, detail="Unknown job status")