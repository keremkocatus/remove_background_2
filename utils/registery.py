import uuid
from fastapi import HTTPException

JOB_REGISTRY: dict[str, dict] = {}

# Register a new background-removal job and return its identifier
def register_job(
    image_url: str,
    user_id: str,
    bucket_id: str,
    category: str,
    is_long_top: bool = False,
) -> str:
    job_id = str(uuid.uuid4())

    JOB_REGISTRY[job_id] = {
        "enhance_status": "processing",
        "rembg_status": "processing",
        "caption_status": "processing",
        "enhance_prediction_id": None,
        "rembg_prediction_id": None,
        "wardrobe_id": None,
        "user_id": user_id,
        "bucket_id": bucket_id,
        "image_url": image_url,
        "category": category,
        "is_long_top": is_long_top,
        "rembg_url": None,
        "enhance_url": None,
    }
    return job_id

def get_job_by_id(job_id):
    return JOB_REGISTRY.get(job_id)

def get_job_id_by_job(job: dict):
    for jid, record in JOB_REGISTRY.items():
        if record is job or record == job:
            return jid
    raise ValueError("No job found matching the provided job dict")

def get_job_by_prediction_id(prediction_id: str, is_enhance: bool) -> tuple[str, dict]:
    for job_id, job in JOB_REGISTRY.items():
        if is_enhance:
            if job.get("enhance_prediction_id") == prediction_id:
                return job_id, job
        else:
            if job.get("rembg_prediction_id") == prediction_id:
                return job_id, job

    raise ValueError(f"No job found with prediction ID: {prediction_id}")

def update_registry(job_id: str, key: str, new_value):
    job = JOB_REGISTRY.get(job_id)
    if not job:
        raise ValueError(f"No job found with job ID: {job_id}")
    
    if key not in job:
        raise KeyError(f"Key '{key}' not found in the job with ID: {job_id}")
    
    job[key] = new_value

def get_job_status(job_id: str, is_enhance: bool):
    job = JOB_REGISTRY.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} bulunamadı")

    if is_enhance:
        if job["enhance_status"] == "finished" and job["rembg_status"] == "finished" and job["caption_status"] == "finished":
            result_url = job["rembg_url"]
            # DEL KOMUTU
            return {"job_id": job_id, "status": "finished", "result_url": result_url}
        else:
            return {"job_id": job_id, "status": "processing"}
    else:
        if job["rembg_status"] == "finished" and job["caption_status"] == "finished":
            result_url = job["rembg_url"]
            # DEL KOMUTU
            return {"job_id": job_id, "status": "finished", "result_url": result_url}
        else:
            return {"job_id": job_id, "status": "processing"}