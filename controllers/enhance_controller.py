import asyncio
from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from services.replicate_enhance_service import get_job_status, register_job, trigger_prediction

router = APIRouter()

@router.post("/enhance-image")
async def enhance_image(user_id: str = Form(...), clothe_image: UploadFile = File(...)):
    try:
    # Todo upload supabase
        job_id = register_job(clothe_image, user_id)
    # Todo insert jop record

        loop = asyncio.get_running_loop()
        loop.create_task(trigger_prediction(job_id))

        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in enhance image: {e}"
        )
    
@router.get("/job-status/{job_id}")
async def fetch_job_status(job_id: str):
    try:
        return await get_job_status(job_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching job status for {job_id}: {e}"
        )