from utils.image_utils import process_mask, get_image_from_url
from services.supabase_wardrobe_service import upload_background_removed_image, mark_job_failed, upload_enhanced_image
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

async def start_fast_background_process(prediction: dict, job_id: str, job: dict[str, str]):
    try:
        img = await run_in_threadpool(get_image_from_url,prediction["output"])
        result_url = await upload_background_removed_image(img, job_id, job)
        
        job["status"] = "finished"
        job["result_url"] = result_url

    except Exception as error:
        await mark_job_failed(job_id)
        print(f"Error in start_fast_background_process for job {job_id}: {error}")
        raise

async def start_enhance_background_process(prediction: dict, job_id: str, job: dict[str, str]):
    try:
        img = await run_in_threadpool(get_image_from_url,prediction["output"])
        result_url = await upload_enhanced_image(img, job_id, job)
        
        job["status"] = "finished"
        job["result_url"] = result_url

    except Exception as error:
        await mark_job_failed(job_id)
        print(f"Error in start_enhance_background_process for job {job_id}: {error}")
        raise