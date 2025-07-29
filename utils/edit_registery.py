import uuid
from fastapi import HTTPException
from utils.error_logger import upload_error_log


EDIT_REGISTRY: dict[str, dict] = {}

# Register a new background-removal job and return its identifier
def register_edit_job(
    image_url: str,
    user_id: str,
    prompt: str,
    bucket_id: str,
) -> str:
    job_id = str(uuid.uuid4())

    EDIT_REGISTRY[job_id] = {
        "status": "processing",
        "prediction_id": None,
        "user_id": user_id,
        "bucket_id": bucket_id,
        "image_url": image_url,
        "edited_image_url": None,
        "prompt": prompt
    }
    return job_id

def get_edit_job_by_id(job_id):
    return EDIT_REGISTRY.get(job_id)

def get_edit_job_id_by_job(job: dict):
    for jid, record in EDIT_REGISTRY.items():
        if record is job or record == job:
            return jid
    raise ValueError("No job found matching the provided job dict")


def get_edit_job_by_prediction_id(prediction_id: str, is_enhance: bool) -> tuple[str, dict]:
    for job_id, job in EDIT_REGISTRY.items():
       
        if job.get("prediction_id") == prediction_id:
            return job_id, job

    raise ValueError(f"No job found with prediction ID: {prediction_id}")


def update_edit_registry(job_id: str, key: str, new_value):
    job = EDIT_REGISTRY.get(job_id)
    if not job:
        raise ValueError(f"No job found with job ID: {job_id}")

    if key not in job:
        raise KeyError(f"Key '{key}' not found in the job with ID: {job_id}")

    job[key] = new_value


async def get_edit_job_status(job_id: str):
    job = EDIT_REGISTRY.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} bulunamadı")

    status = job.get("status")
   
    if status == "finished":
        result_url = job["edited_image_url"]
        del EDIT_REGISTRY[job_id]

        return {
            "job_id": job_id,
            "status": "finished",
            "edited_image_url": result_url,
        }
    elif status == "failed":
        job = get_edit_job_by_id(job_id)
        await upload_error_log(job["user_id"], job["image_url"], job_id, failed_tasks=[])
        del EDIT_REGISTRY[job_id]

        return {
            "job_id": job_id,
            "status": "failed",
        }
    else:
        return {"job_id": job_id, "status": "processing"}

