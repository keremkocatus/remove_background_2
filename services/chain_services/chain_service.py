import asyncio
from services.caption_services.caption_service import get_caption_for_image
from services.replicate_services.rembg_service import (
    get_job_by_id as get_rembg_job,
    trigger_rembg,
)

async def chain_remove_background(job_id: str):
    """
    Zincirleme fonksiyon: önce caption, sonra background removal.
    """
    try:
        job = get_rembg_job(job_id)
        loop = asyncio.get_running_loop()

        # 1) Caption
        loop.create_task(get_caption_for_image(job))
        # 2) Background removal
        loop.create_task(trigger_rembg(job_id))
    except Exception as e:
        print(f"[chain_remove_background] Error: {e}")