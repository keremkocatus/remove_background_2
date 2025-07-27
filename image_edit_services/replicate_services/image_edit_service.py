import os
import replicate
import logging
from fastapi import HTTPException
from dotenv import load_dotenv
from replicate.exceptions import ReplicateError
from services.supabase_services.fail_service import mark_edit_job_failed
from utils.background_utils import start_edit_background_process
from utils.edit_registery import get_edit_job_by_id, get_edit_job_by_prediction_id, update_edit_registry

load_dotenv()
replicate_api_token = os.getenv("REPLICATE_API_TOKEN")
replicate_client = replicate.Client(api_token=replicate_api_token)

MODEL_ID = os.getenv("ENHANCE_MODEL_ID")
EDIT_WEBHOOK_URL = f"{os.getenv('REPLICATE_WEBHOOK_URL')}/webhook/edit-image"

# Submit an asynchronous enhancement prediction request to Replicate
async def trigger_edit_prediction(job_id: str) -> None:
    try:
        job = get_edit_job_by_id(job_id)

        prediction_input = {
            "prompt": job["prompt"],
            "input_image": job["image_url"],
            "output_format": "jpg"
        }

        prediction = await replicate_client.predictions.async_create(
            version=MODEL_ID,
            input=prediction_input,
            webhook=EDIT_WEBHOOK_URL,
            webhook_events_filter=["completed"],
        )

        # Prediction başarılı, registry güncelle
        update_edit_registry(job_id, "prediction_id", prediction.id)

    except ReplicateError as e:
        logging.error(f"[trigger_prediction] ReplicateError for job {job_id}: {e}")
        # Job'u failed olarak işaretle
        await mark_edit_job_failed(job_id)

    except Exception as e:
        logging.exception(f"[trigger_prediction] Unexpected error for job {job_id}")
        await mark_edit_job_failed(job_id)

# Handle webhook event for enhancement prediction completion
async def handle_edit_webhook(payload: dict) -> None:
    job_id = None
    try:
        status = payload.get("status")

        if status == "succeeded":
            prediction_id = payload.get("id")
            job_id, job = get_edit_job_by_prediction_id(prediction_id, is_enhance=True)

            await start_edit_background_process(payload, job_id, job)

            return job_id, job
        else: 
            await mark_edit_job_failed(job_id)
    except Exception as e:
        if job_id:
            await mark_edit_job_failed(job_id)
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {e}")


