import uuid

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
        "status": "processing",
        "prediction_id": None,
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

def get_job_by_prediction_id(prediction_id: str) -> tuple[str, dict]:
    for job_id, job in JOB_REGISTRY.items():
        if job.get("prediction_id") == prediction_id:
            return job_id, job
    raise ValueError(f"No job found with prediction ID: {prediction_id}")

def update_registry(job_id: str, key: str, new_value):
    job = JOB_REGISTRY.get(job_id)
    if not job:
        raise ValueError(f"No job found with job ID: {job_id}")
    
    if key not in job:
        raise KeyError(f"Key '{key}' not found in the job with ID: {job_id}")
    
    job[key] = new_value

