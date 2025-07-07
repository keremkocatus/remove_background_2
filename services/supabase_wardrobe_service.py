import os
import uuid
import asyncio
from dotenv import load_dotenv
from fastapi import UploadFile
from supabase import AsyncClient, create_async_client
from utils.url_utils import clean_url
from services.openai_service import generate_image_caption

load_dotenv()

WARDROBE_BUCKET = os.getenv("SUPABASE_URL")
WARDROBE_KEY = os.getenv("SUPABASE_ANON_KEY")
BUCKET_NAME = "wardrobe"

# Lazy-initialized Supabase client
_supabase_client: AsyncClient | None = None
_supabase_lock = asyncio.Lock()

async def get_supabase_client() -> AsyncClient:
    global _supabase_client
    if _supabase_client is None:
        async with _supabase_lock:
            if _supabase_client is None:
                _supabase_client = await create_async_client(WARDROBE_BUCKET, WARDROBE_KEY)
    return _supabase_client

async def upload_original_image(user_id: str, image_file: UploadFile, category: str) -> tuple[str, str]:
    try:
        supabase = await get_supabase_client()
        image_data = await image_file.read()
        bucket_id = str(uuid.uuid4())
        storage_path = f"{user_id}/{bucket_id}/{category}.jpg"

        upload_response = await supabase.storage.from_(BUCKET_NAME).upload(
            file=image_data,
            path=storage_path,
            file_options={"cache-control": "3600", "upsert": "false"}
        )

        public_url_response = await supabase.storage.from_(BUCKET_NAME).get_public_url(storage_path)
        if isinstance(public_url_response, str):
            public_url = clean_url(public_url_response)
        else:
            public_url = clean_url(public_url_response.get("publicURL") or public_url_response.get("public_url"))

        return public_url, bucket_id
    except Exception as error:
        print(f"Error in upload_original_image: {error}")
        return None

async def insert_job_record(job_id: str, image_url: str, user_id: str, category: str, is_long_top: bool = False) -> dict:
    try:
        print(image_url)
        supabase = await get_supabase_client()
        caption = await get_caption_of_image(image_url, category)
        response = await supabase.from_(BUCKET_NAME).insert({
            "image_url": image_url,
            "user_id": user_id,
            "category": category,
            "is_long_top": is_long_top,
            "job_id": job_id,
            "status": "processing",
            "caption": caption
        }).execute()
        
        return {"status": "Job successfully inserted into database"}
    except Exception as error:
        print(f"Error in insert_job_record: {error}")
        return None

async def upload_background_removed_image(processed_image: bytes, job_id: str, job: dict[str, str]) -> str:
    try:
        supabase = await get_supabase_client()
        storage_path = f"{job['user_id']}/{job['bucket_id']}/bg_removed_{job['category']}.png"

        upload_response = await supabase.storage.from_(BUCKET_NAME).upload(
            file=processed_image,
            path=storage_path,
            file_options={"cache-control": "3600", "upsert": "false"}
        )

        public_url_response = await supabase.storage.from_(BUCKET_NAME).get_public_url(storage_path)
        if isinstance(public_url_response, str):
            public_url = clean_url(public_url_response)
        else:
            public_url = clean_url(public_url_response.get("publicURL") or public_url_response.get("public_url"))

        update_response = await supabase.from_(BUCKET_NAME).update({
            "removed_bg_image_url": public_url,
            "status": "finished"
        }).eq("job_id", job_id).execute()

        return public_url
    except Exception as error:
        print(f"Error in upload_background_removed_image: {error}")
        return None

async def mark_job_failed(job_id: str) -> None:
    supabase = await get_supabase_client()
    await supabase.from_(BUCKET_NAME).update({
        "status": "failed"
    }).eq("job_id", job_id).execute()

async def get_caption_of_image(image_url: str, category: str) -> str:
    """
    Get or generate a caption for an image using ChatGPT based on its category
    
    Args:
        image_url: The URL of the image to get caption for
    
    Returns:
        Generated caption as a string
    """
    try:
        supabase = await get_supabase_client()
        
        # First, check if we already have a caption    
        # If no caption exists, generate one using ChatGPT

        print("Generating caption")
        caption = await generate_image_caption(image_url, category)
        print("Caption generated", caption)
            # Save the generated caption back to the database
        await supabase.from_(BUCKET_NAME).update({
                "caption": caption
            }).eq("image_url", image_url).execute()
            
        return caption
    except Exception as error:
            # Image not found in database
            return "Image not found in database"
            
    except Exception as error:
        print(f"Error in get_caption_of_image: {error}")
        return "Error generating caption"