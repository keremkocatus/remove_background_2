from services.supabase_services.client_service import get_supabase_client
from utils.caption_tools.hex_utils import convert_colors_to_hex_format
from utils.edit_registery import get_edit_job_by_id
from utils.extract_utils import extract_id
from utils.review_registery import get_review_job_id_by_job
from utils.wardrobe_registery import get_job_by_id, update_registry
from core import config

WARDROBE_BUCKET_NAME = config.WARDROBE_BUCKET_NAME
CLOTHES_DETAIL_TABLE = config.CLOTHES_DETAIL_TABLE
EDIT_BUCKET_NAME = config.EDIT_BUCKET_NAME
EDIT_TABLE_NAME = config.EDIT_TABLE_NAME
REVIEW_TABLE = config.REVIEW_TABLE


async def insert_job_record(job_id: str) -> dict:
    try:
        supabase = await get_supabase_client()
        job = get_job_by_id(job_id)

        response = await supabase.from_(WARDROBE_BUCKET_NAME).insert({
            "image_url": job["image_url"],
            "user_id": job["user_id"],
            "category": job["category"],
            "is_long_top": job["is_long_top"],
            "job_id": job_id,
            "enhance_status": job["enhance_status"],
            "rembg_status": job["rembg_status"]
        }).execute()

        update_registry(job_id, "wardrobe_id", extract_id(response.data))

        return {"status": "Job successfully inserted into database"}
    except Exception as error:
        print(f"Error in insert_job_record: {error}")
        return None


async def update_job_record(job_id: str) -> dict:
    try:
        supabase = await get_supabase_client()
        job = get_job_by_id(job_id)

        response = await supabase.from_(WARDROBE_BUCKET_NAME).update({
            "job_id": job_id,
            "enhance_status": job["enhance_status"],
            "rembg_status": job["rembg_status"],
            "caption_status": job["caption_status"],
        }).eq("image_url", job["image_url"]).execute()

        return {"status": "Job successfully updated into database"}
    except Exception as error:
        print(f"Error in update_job_record: {error}")
        return None


async def insert_clothes_detail(
    wardrobe_item_id: str, user_id: str, caption_data: dict
) -> dict:
    """
    Insert structured clothing details into clothes_detail table
    """
    try:
        supabase = await get_supabase_client()

        # Convert color names to hex format
        color_names = caption_data.get("colors", [])
        colors_with_hex = convert_colors_to_hex_format(color_names)

        detail_record = {
            "wardrobe_item_id": wardrobe_item_id,
            "user_id": user_id,
            "name": caption_data.get("brief_caption", "Clothing Item"),
            "category": caption_data.get("category", "Unknown"),
            "material": caption_data.get("material", "Cotton"),
            "style": caption_data.get("style", "Casual"),
            "colors": colors_with_hex,
            "seasons": caption_data.get("seasons", []),
            "notes": caption_data.get("ai_context", "Add a note..."),
        }

        await supabase.from_(CLOTHES_DETAIL_TABLE).insert(detail_record).execute()

        return {"status": "Clothes detail successfully inserted"}
    except Exception as error:
        print(f"Error in insert_clothes_detail: {error}")
        return None


async def insert_edit_job_record(job_id: str) -> dict:
    try:
        supabase = await get_supabase_client()
        job = get_edit_job_by_id(job_id)

        await supabase.from_(EDIT_TABLE_NAME).insert({
            "image_url": job["image_url"],
            "user_id": job["user_id"],
            "job_id": job_id,
            "status": job["status"],
            "prompt": job["prompt"],
        }).execute()

        return {"status": "Job successfully inserted into database"}
    except Exception as error:
        print(f"Error in insert_edit_job_record: {error}")
        return None


async def insert_review_job_record(job: dict, result) -> dict:
    try:
        supabase = await get_supabase_client()
        job_id = get_review_job_id_by_job(job)

        await supabase.from_(REVIEW_TABLE).insert({
            "image_url": job["image_url"],
            "user_id": job["user_id"],
            "job_id": job_id,
            "status": "finished",
            "roast_level": job["roast_level"],
            "result": result,
        }).execute()

        return {"status": "Job successfully inserted into database"}
    except Exception as error:
        print(f"Error in insert_review_job_record: {error}")
        return None
