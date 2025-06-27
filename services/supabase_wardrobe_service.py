import os
import uuid
import asyncio
from dotenv import load_dotenv
from fastapi import UploadFile
from supabase import AsyncClient, create_async_client
from utils.url_utils import clean_url

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_TABLE = "deneme"

# lazy-init Supabase client
_supabase: AsyncClient | None = None
_supabase_lock = asyncio.Lock()

async def _get_supabase() -> AsyncClient:
    global _supabase
    if _supabase is None:
        async with _supabase_lock:
            if _supabase is None:
                _supabase = await create_async_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase

# Upload original clothing image to Supabase
async def upload_supabase(user_id: str, clothe_image: UploadFile, category: str) -> tuple[str, str]:
    try:
        supabase = await _get_supabase()
        byte_image = await clothe_image.read()
        bucket_uuid = str(uuid.uuid4())
        img_path = f"{user_id}/{bucket_uuid}/{category}.jpg"

        resp = await supabase.storage.from_(SUPABASE_TABLE).upload(
            file=byte_image,
            path=img_path,
            file_options={"cache-control": "3600", "upsert": "false"}
        )

        url_response = await supabase.storage.from_(SUPABASE_TABLE).get_public_url(img_path)
        
        if isinstance(url_response, str):
            public_url = clean_url(url_response)
        elif isinstance(url_response, dict):
            public_url = clean_url(url_response["publicURL"] or url_response["public_url"])
        else:
            print("Public URL type error!")
    
        return public_url, bucket_uuid

    except Exception as e:
        print(f"Error in upload_supabase: {e}")
        return None

# Insert a new job record into Supabase table
async def insert_supabase(job_id: str, img_url: str, user_id: str, category: str, is_long_top: bool) -> str:
    try:
        supabase = await _get_supabase()

        resp = await supabase.table(SUPABASE_TABLE).insert({
            "image_url": img_url,
            "user_id": user_id,
            "category": category,
            "is_long_top": is_long_top,
            "job_id": job_id
        }).execute()
        print("test")
        return {"status": "Job successfully inserted database!"}

    except Exception as e:
        print(f"Error in insert_supabase: {e}")
        return None

# Upload background-removed image and update job record
async def upload_bg_removed(bg_removed_image: bytes, job_id: str, job: dict[str, str]) -> str:
    try:
        supabase = await _get_supabase()
        img_path = f"{job['user_id']}/{job['bucket_uuid']}/bg_removed_{job['category']}.png"

        resp = await supabase.storage.from_(SUPABASE_TABLE).upload(
            file=bg_removed_image,
            path=img_path,
            file_options={"cache-control": "3600", "upsert": "false"}
        )

        url_response = await supabase.storage.from_(SUPABASE_TABLE).get_public_url(img_path)
        
        if isinstance(url_response, str):
            public_url = clean_url(url_response)
        elif isinstance(url_response, dict):
            public_url = clean_url(url_response["publicURL"] or url_response["public_url"])
        else:
            print("Public URL type error!")

        resp = await supabase.table(SUPABASE_TABLE).update({
            "removed_bg_image_url": public_url
        }).eq("job_id", job_id).execute()

        return public_url

    except Exception as e:
        print(f"Error in upload_bg_removed: {e}")
        return None
