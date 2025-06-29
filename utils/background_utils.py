from utils.image_utils import process_mask
from services.supabase_wardrobe_service import upload_background_removed_image, mark_job_failed
from starlette.concurrency import run_in_threadpool

async def start_quality_background_process(prediction: dict, job_id: str, job: dict[str, str]):
    try:
        for i, item in enumerate(prediction["output"]):
            if i == 2:
                mask_url = item

        processed_image = await run_in_threadpool(process_mask, mask_url, job)
        result_url = await upload_background_removed_image(processed_image, job_id, job)
        
        job["status"] = "finished"
        job["result_url"] = result_url

    except Exception as error:
        await mark_job_failed(job_id)
        print(f"Error in start_quality_background_process for job {job_id}: {error}")
        raise

async def start_low_quality_background_process(prediction: dict, job_id: str, job: dict[str, str]):
    try:
        print(prediction["output"])
        print(type(prediction["output"]))

    except Exception as error:
        await mark_job_failed(job_id)
        print(f"Error in start_low_quality_background_process for job {job_id}: {error}")
        raise
