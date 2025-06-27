import os
import uuid
import replicate
from utils.prompt_utils import get_mask_prompts
from fastapi import HTTPException
from utils.background_utils import start_background_process
from dotenv import load_dotenv
import asyncio

load_dotenv()
REPL_TOKEN = os.getenv("REPLICATE_API_TOKEN")
_client = replicate.Client(api_token=REPL_TOKEN)

MODEL_VERSION = "ee871c19efb1941f55f66a3d7d960428c8a5afcb77449547fe8e5a3ab9ebc21c"
JOBS: dict[str, dict] = {}

# Create and register a new background-removal job
def create_job(img_url: str, user_id: str, bucket_uuid: str, category: str, is_long_top: bool):
    try:
        job_id = str(uuid.uuid4())
        JOBS[job_id] = {
            "status": "processing",
            "is_prediction_finished": False,
            "prediction_id": None,
            "user_id": user_id,
            "bucket_uuid": bucket_uuid,
            "public_url": img_url,
            "category": category,
            "is_long_top": is_long_top,
            "result_url": None
        }
        return job_id
    except Exception as e:
        print(f"Error in create_job: {e}")
        raise

# Kick off the Replicate prediction asynchronously
async def start_replicate_prediction(job_id: str):
    try:
        job = JOBS[job_id]
        mask_prompt, negative_mask_prompt = get_mask_prompts(job["category"], job["is_long_top"])
        input = {
            "image": job["public_url"],
            "mask_prompt": mask_prompt,
            "adjustment_factor": -20,
            "negative_mask_prompt": negative_mask_prompt,
        }
        prediction = await _client.predictions.async_create(
            version=MODEL_VERSION,
            input=input
        )
        JOBS[job_id]["prediction_id"] = prediction.id
    except Exception as e:
        print(f"Error in start_replicate_prediction for job {job_id}: {e}")
        raise

# Check status of a job and, if succeeded, start post-processing
async def check_job_status(job_id: str):
    try:
        job = JOBS.get(job_id)
        if not job:
            raise HTTPException(404, "Job not exist!")

        if job["status"] == "processing" and not job["is_prediction_finished"]:
            pred = await _client.predictions.async_get(job["prediction_id"])
            if pred.status == "succeeded":
                job["is_prediction_finished"] = True
                loop = asyncio.get_running_loop()
                loop.create_task(start_background_process(pred, job_id, job))
                return {"status": "processing"}
            elif pred.status == "canceled":
                return {"status": "canceled"}
            elif pred.status == "failed":
                return {"status": "failed"}
            else:
                return {"status": "processing"}

        if job["status"] == "processing" and job["is_prediction_finished"]:
            return {"status": "processing"}

        if job["status"] == "finished" and job["is_prediction_finished"]:
            return {"status": "finished", "result_url": job["result_url"]}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in check_job_status for job {job_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
