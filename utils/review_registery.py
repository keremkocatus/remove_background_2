import uuid
from fastapi import HTTPException
from utils.error_logger import upload_error_log

REVIEW_REGISTRY: dict[str, dict] = {}

# Register a new outfit review job and return its identifier
def register_review_job(
    image_url: str,
    user_id: str,
    roast_level: int,
    bucket_id: str,
) -> str:
    job_id = str(uuid.uuid4())

    REVIEW_REGISTRY[job_id] = {
        "status": "processing",
        "user_id": user_id,
        "bucket_id": bucket_id,
        "image_url": image_url,
        "roast_level": roast_level,
        "result": None
    }
    return job_id


def get_review_job_by_id(job_id: str) -> dict | None:
    return REVIEW_REGISTRY.get(job_id)


def get_review_job_id_by_job(job: dict) -> str:
    for jid, record in REVIEW_REGISTRY.items():
        if record is job or record == job:
            return jid
    raise ValueError("No review job found matching the provided job dict")


def update_review_registry(job_id: str, key: str, new_value):
    job = REVIEW_REGISTRY.get(job_id)
    if not job:
        raise ValueError(f"No review job found with job ID: {job_id}")

    if key not in job:
        raise KeyError(f"Key '{key}' not found in the review job with ID: {job_id}")

    job[key] = new_value


async def get_review_job_status(job_id: str):
    job = REVIEW_REGISTRY.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Review job {job_id} not found")

    status = job.get("status")

    if status == "finished":
        result = job["result"]
        del REVIEW_REGISTRY[job_id]

        return {
            "job_id": job_id,
            "status": "finished",
            "result": result,
        }
    elif status == "failed":
        await upload_error_log(job["user_id"], job["image_url"], job_id, failed_tasks=[])
        del REVIEW_REGISTRY[job_id]

        return {
            "job_id": job_id,
            "status": "failed",
        }
    else:
        return {
            "job_id": job_id,
            "status": "processing"
        }
