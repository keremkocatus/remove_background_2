from utils.image_utils import process_mask
from services.supabase_wardrobe_service import upload_bg_removed
from starlette.concurrency import run_in_threadpool
from replicate.prediction import Prediction

# Handle background mask processing and upload
async def start_background_process(pred: Prediction, job_id: str, job: dict[str, str]):
    try:
        for i, item in enumerate(pred.output):
            if i == 2:
                mask_url = item

        bg_removed_image = await run_in_threadpool(process_mask, mask_url, job)
        result_url = await upload_bg_removed(bg_removed_image, job_id, job)

        job["status"] = "finished"
        job["result_url"] = result_url
    except Exception as e:
        print(f"Error in start_background_process for job {job_id}: {e}")
        raise
