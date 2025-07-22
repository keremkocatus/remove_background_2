import os
import replicate
import asyncio
from fastapi import HTTPException
from dotenv import load_dotenv

from services.supabase_services.fail_service import mark_job_failed

from utils.background_utils import start_fast_background_process

from utils.registery import (
    get_job_by_id,
    get_job_by_prediction_id,
    update_registry,
)

load_dotenv()
replicate_api_token = os.getenv("REPLICATE_API_TOKEN")
replicate_client = replicate.Client(api_token=replicate_api_token)

FAST_MODEL_ID = os.getenv("FAST_MODEL_ID")
REMBG_WEBHOOK_URL = os.getenv("REPLICATE_WEBHOOK_URL")

# Submit an asynchronous prediction request to Replicate
async def trigger_rembg(job_id: str):
    job = get_job_by_id(job_id)

    if job["enhance_url"] is not None:
        image_url = job["enhance_url"]
    else:
        image_url = job["image_url"]

    prediction_input = {
        "image": image_url,
        "format": "png",
        "reverse": False,
        "threshold": -20,
        "background_type": "rgba",
    }
    
    model_id = FAST_MODEL_ID
    webhook_url = f"{REMBG_WEBHOOK_URL}/rembg/webhook/replicate/fast"

    prediction = await replicate_client.predictions.async_create(
        version=model_id,
        input=prediction_input,
        webhook=webhook_url,
        webhook_events_filter=["completed"],
    )
    # prediction_id bilgisini registry'ye yaz
    update_registry(job_id, "rembg_prediction_id", prediction.id)

# Handle webhook event for fast prediction completion
async def handle_fast_webhook(payload: dict):
    job_id = None
    try:
        prediction_id = payload["id"]
        job_id, job = get_job_by_prediction_id(prediction_id, is_enhance=False)

        loop = asyncio.get_running_loop()
        loop.create_task(start_fast_background_process(payload, job_id, job))
    except Exception as e:
        if job_id:
            await mark_job_failed(job_id)
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {e}")

