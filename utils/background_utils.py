from starlette.concurrency import run_in_threadpool

from services.caption_services.caption_service import get_caption_for_image
from utils.image_utils import process_mask, get_image_from_url
from services.supabase_services.upload_service import upload_background_removed_image, upload_enhanced_image
from services.supabase_services.fail_service import mark_job_failed

async def start_quality_background_process(prediction: dict, job_id: str, job: dict[str, str]):
    try:
        for i, item in enumerate(prediction["output"]):
            if i == 2:
                mask_url = item

        processed_image = await run_in_threadpool(process_mask, mask_url, job)
        result_url = await upload_background_removed_image(processed_image, job_id, job)
        
        job["status"] = "finished"
        job["rembg_url"] = result_url

    except Exception as error:
        await mark_job_failed(job_id)
        print(f"Error in start_quality_background_process for job {job_id}: {error}")
        raise

async def start_fast_background_process(prediction: dict, job_id: str, job: dict[str, str]):
    try:
        img = await run_in_threadpool(get_image_from_url,prediction["output"])
        result_url = await upload_background_removed_image(img, job_id, job)
        
        job["rembg_status"] = "finished"
        job["rembg_url"] = result_url

    except Exception as error:
        await mark_job_failed(job_id)
        print(f"Error in start_fast_background_process for job {job_id}: {error}")
        raise

async def start_enhance_background_process(prediction: dict, job_id: str, job: dict[str, str]):
    try:
        img = await run_in_threadpool(get_image_from_url,prediction["output"])
        result_url = await upload_enhanced_image(img, job)
        
        job["enhance_status"] = "finished"
        job["enhance_url"] = result_url

    except Exception as error:
        print(f"Error in start_enhance_background_process for job {job_id}: {error}")
        raise

async def start_caption_background_process(image_url):
    try:
        caption = await get_caption_for_image(image_url)

        return caption
    except Exception as error:
        print(f"Error in start_caption_background_process: {error}")
        raise