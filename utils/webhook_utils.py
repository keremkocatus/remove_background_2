from fastapi import HTTPException

def get_job_id_by_prediction(prediction_id: str, JOBS: dict[str,dict]) -> tuple[str, dict[str,str]]: 
    
    for job_id, job in JOBS.items():
        if job.get("prediction_id") == prediction_id:
            return job_id, job
    raise HTTPException(404, f"Job with prediction_id={prediction_id} not found")