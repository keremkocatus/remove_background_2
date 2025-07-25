import asyncio
import os
import replicate
import logging
from fastapi import HTTPException
from dotenv import load_dotenv
from replicate.exceptions import ReplicateError
from services.supabase_services.fail_service import mark_job_failed
from utils.background_utils import start_enhance_background_process
from utils.registery import get_job_by_id, get_job_by_prediction_id, update_registry
from utils.prompt_utils import get_enhance_prompt
import asyncio
from services.replicate_services.rembg_service import trigger_rembg

load_dotenv()
replicate_api_token = os.getenv("REPLICATE_API_TOKEN")
replicate_client = replicate.Client(api_token=replicate_api_token)

MODEL_ID = os.getenv("ENHANCE_MODEL_ID")
ENHANCE_WEBHOOK_URL = f"{os.getenv('REPLICATE_WEBHOOK_URL')}/webhook/late-enhance"

# Submit an asynchronous enhancement prediction request to Replicate
async def trigger_late_enhance(job_id: str) -> None:
    try:
        job = get_job_by_id(job_id)
        image_url = job["image_url"]
        category = job["category"]
        
        prompt = get_enhance_prompt(category)

        prediction_input = {
            "prompt": prompt,
            "input_image": image_url,
            "output_format": "jpg"
        }

        prediction = await replicate_client.predictions.async_create(
            version=MODEL_ID,
            input=prediction_input,
            webhook=ENHANCE_WEBHOOK_URL,
            webhook_events_filter=["completed"],
        )

        # Prediction başarılı, registry güncelle
        update_registry(job_id, "enhance_prediction_id", prediction.id)

    except ReplicateError as e:
        logging.error(f"[late enhance] ReplicateError for job {job_id}: {e}")
        # Job'u failed olarak işaretle
        await mark_job_failed(job_id)

    except Exception as e:
        logging.exception(f"[late enhance] Unexpected error for job {job_id}")
        await mark_job_failed(job_id)

# Handle webhook event for enhancement prediction completion
async def handle_late_enhance_webhook(payload: dict) -> None:
    job_id = None
    try:
        prediction_id = payload.get("id")
        job_id, job = get_job_by_prediction_id(prediction_id, is_enhance=True)

        await start_enhance_background_process(payload, job_id, job)

        return job_id, job
    except Exception as e:
        if job_id:
            await mark_job_failed(job_id)
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {e}")


async def late_chain_remove_background(job_id: str):
    """
    late enhance fonksiyonu
    """
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(trigger_rembg(job_id))
    except Exception as e:
        print(f"[chain_remove_background] Error: {e}")
