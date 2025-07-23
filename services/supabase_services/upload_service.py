import os
import uuid
from fastapi import UploadFile
from services.supabase_services.client_service import get_supabase_client
from utils.url_utils import clean_url

BUCKET_NAME = os.getenv("WARDROBE_BUCKET_NAME")

def build_storage_path(user_id: str, bucket_id: str, filename: str) -> str:
    return f"{user_id}/{bucket_id}/{filename}"

def extract_public_url(response: dict | str) -> str:
    if isinstance(response, str):
        return clean_url(response)
    return clean_url(response.get("publicURL") or response.get("public_url"))

async def upload_image(user_id: str, image_file: UploadFile, category: str) -> tuple[str, str] | None:
    try:
        supabase = await get_supabase_client()
        image_data = await image_file.read()
        bucket_id = str(uuid.uuid4())
        storage_path = build_storage_path(user_id, bucket_id, f"{category}.jpg")

        await supabase.storage.from_(BUCKET_NAME).upload(
            file=image_data,
            path=storage_path,
            file_options={"cache-control": "3600", "upsert": "false"},
        )

        public_url_response = await supabase.storage.from_(BUCKET_NAME).get_public_url(storage_path)
        public_url = extract_public_url(public_url_response)

        return public_url, bucket_id
    except Exception as error:
        print(f"Error in upload_image: {error}")
        return None

async def upload_background_removed_image(processed_image: bytes, job_id: str, job: dict[str, str]) -> str | None:
    try:
        supabase = await get_supabase_client()
        storage_path = build_storage_path(job["user_id"], job["bucket_id"], f"bg_removed_{job['category']}.png")

        await supabase.storage.from_(BUCKET_NAME).upload(
            file=processed_image,
            path=storage_path,
            file_options={"cache-control": "3600", "upsert": "true"},
        )

        public_url_response = await supabase.storage.from_(BUCKET_NAME).get_public_url(storage_path)
        public_url = extract_public_url(public_url_response)

        await supabase.from_(BUCKET_NAME).update({
            "removed_bg_image_url": public_url,
            "rembg_status": "finished"
        }).eq("job_id", job_id).execute()

        return public_url
    except Exception as error:
        print(f"Error in upload_background_removed_image: {error}")
        return None

async def upload_enhanced_image(processed_image: bytes, job: dict[str, str]) -> str | None:
    try:
        supabase = await get_supabase_client()
        storage_path = build_storage_path(job["user_id"], job["bucket_id"], "enhanced.png")

        await supabase.storage.from_(BUCKET_NAME).upload(
            file=processed_image,
            path=storage_path,
            file_options={"cache-control": "3600", "upsert": "true"},
        )

        public_url_response = await supabase.storage.from_(BUCKET_NAME).get_public_url(storage_path)
        public_url = extract_public_url(public_url_response)

        await supabase.from_(BUCKET_NAME).update({
            "enhanced_image_url": public_url,
            "enhance_status": "finished"
        }).eq("image_url", job["image_url"]).execute()

        return public_url
    except Exception as error:
        print(f"Error in upload_enhanced_image: {error}")
        return None
