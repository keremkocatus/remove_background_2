import os
import replicate
import asyncio
from fastapi import HTTPException
from dotenv import load_dotenv
from services.supabase_services.fail_service import mark_job_failed
from utils.background_utils import start_enhance_background_process
from utils.registery import get_job_by_id, get_job_by_prediction_id, update_registry

load_dotenv()
replicate_api_token = os.getenv("REPLICATE_API_TOKEN")
replicate_client = replicate.Client(api_token=replicate_api_token)

MODEL_ID = os.getenv("ENHANCE_MODEL_ID")
ENHANCE_WEBHOOK_URL = f"{os.getenv('REPLICATE_WEBHOOK_URL')}/enhance/webhook/replicate-enhance"

# Submit an asynchronous enhancement prediction request to Replicate
async def trigger_prediction(job_id: str) -> None:
    job = get_job_by_id(job_id)

    if job["rembg_url"] is not None:
        image_url = job["rembg_url"]
    else:
        image_url = job["image_url"]

    prediction_input = {
        "prompt": (
            "Please extract the clothing item from the given real-world image and convert it into a clean, flat-lay digital version. "
            "Ensure the shape, proportions, and color of the garment are preserved accurately in the transformation. "
            "Remove the background, accessories, and shadows for a clear, studio-style presentation. "
            "The final output should resemble a catalog image with only the clothing item visible on a plain white or transparent background."
        ),
        "input_image": image_url,
        "output_format": "jpg"
    }

    # Send prediction request
    prediction = await replicate_client.predictions.async_create(
        version=MODEL_ID,
        input=prediction_input,
        webhook=ENHANCE_WEBHOOK_URL,
        webhook_events_filter=["completed"],
    )
    # Update registry with prediction ID
    update_registry(job_id, "prediction_id", prediction.id)

# Handle webhook event for enhancement prediction completion
async def handle_enhance_webhook(payload: dict) -> None:
    job_id = None
    try:
        prediction_id = payload.get("id")
        job_id, job = get_job_by_prediction_id(prediction_id)

        loop = asyncio.get_event_loop()
        loop.create_task(start_enhance_background_process(payload, job_id, job))
    except Exception as e:
        if job_id:
            await mark_job_failed(job_id)
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {e}")

# Retrieve current status of a registered job
async def get_job_status(job_id: str) -> dict:
    job = get_job_by_id(job_id)

    if job["status"] == "processing":
        return {"status": "processing"}

    if job["status"] == "finished":
        result_url = job.get("enhance_url")
        return {"status": "finished", "result_url": result_url}

    raise HTTPException(status_code=500, detail="Unknown job status")
