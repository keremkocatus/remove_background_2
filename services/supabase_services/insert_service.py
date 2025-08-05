from services.supabase_services.client_service import get_supabase_client
from utils.caption_tools.hex_utils import convert_colors_to_hex_format
from utils.extract_utils import extract_id
from utils.registery import get_job_by_id, update_registry
import os

BUCKET_NAME = os.getenv("WARDROBE_BUCKET_NAME")
CLOTHES_DETAIL_TABLE = os.getenv("CLOTHES_DETAIL_TABLE")

async def insert_job_record(job_id: str) -> dict:
    try:
        supabase = await get_supabase_client()
        job = get_job_by_id(job_id)

        response = await supabase.from_(BUCKET_NAME).insert({
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

async def insert_clothes_detail(
    wardrobe_item_id: str, user_id: str, caption_data: dict
) -> dict:
    """
    Insert structured clothing details into clothes_detail table

    Args:
        wardrobe_item_id: UUID of the wardrobe item
        user_id: UUID of the user
        caption_data: Dict from generate_structured_caption containing category, material, style, colors, seasons, etc.

    Returns:
        Success status or None if failed
    """
    try:
        supabase = await get_supabase_client()

        # Convert color names to hex format
        color_names = caption_data.get("colors", [])
        colors_with_hex = convert_colors_to_hex_format(color_names)

        # Extract data from caption_data
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

        response = (
            await supabase.from_(CLOTHES_DETAIL_TABLE).insert(detail_record).execute()
        )

        return {"status": "Clothes detail successfully inserted"}
    except Exception as error:
        print(f"Error in insert_clothes_detail: {error}")
        return None