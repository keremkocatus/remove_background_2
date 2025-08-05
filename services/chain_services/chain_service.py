import asyncio
from services.caption_services.caption_service import process_caption_for_job
from services.replicate_services.rembg_service import trigger_rembg
from utils.wardrobe_registery import get_job_by_id

async def chain_remove_background(job_id: str):
    """
    Zincirleme fonksiyon: önce caption, sonra background removal.
    """
    try:
        job = get_job_by_id(job_id)
        loop = asyncio.get_running_loop()

        # 1) Caption
        loop.create_task(process_caption_for_job(job))
        # 2) Background removal
        loop.create_task(trigger_rembg(job_id))
    except Exception as e:
        print(f"[chain_remove_background] Error: {e}")