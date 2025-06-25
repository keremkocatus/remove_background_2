from supabase import AsyncClient, create_async_client
from fastapi import UploadFile
from utils.url_utils import clean_url
from dotenv import load_dotenv
import uuid
import os

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL")  
SUPABASE_KEY: str = os.getenv("SUPABASE_ANON_KEY") 
supabase: AsyncClient = create_async_client(SUPABASE_URL, SUPABASE_KEY)

SUPABASE_TABLE = "wardrobe"

# Upload original clothing image to Supabase
async def upload_supabase(user_id: str, clothe_image: UploadFile, category: str) -> tuple[str, str]:
    try:
        byte_image = await clothe_image.read()
        bucket_uuid = str(uuid.uuid4())
        img_path = f"{user_id}/{bucket_uuid}/{category}.jpg"
        
        await supabase.storage.from_(SUPABASE_TABLE).upload(
            file=byte_image, 
            path=img_path,
            file_options={"cache-control": "3600", "upsert": "false"}
        )
        
        url_response = supabase.storage.from_(SUPABASE_TABLE).get_public_url(img_path)
        public_url = clean_url(url_response["publicURL"])
        
        return public_url, bucket_uuid
    except Exception as e:
        print(f"Error in upload_supabase: {e}")
        return None

# Insert a new job record into Supabase table
async def insert_supabase(img_url: str, user_id: str, category: str, is_long_top: bool) -> str:
    try:
        job_id = str(uuid.uuid4())
        await supabase.table(SUPABASE_TABLE).insert({
            "image_url": img_url,
            "user_id": user_id,
            "category": category,
            "is_long_top": is_long_top,
            "job_id": job_id
        }).execute()
        return job_id
    except Exception as e:
        print(f"Error in insert_supabase: {e}")
        return None

# Upload background-removed image and update job record
async def upload_bg_removed(bg_removed_image: bytes, job_id: str, job: dict[str, str]):
    try:
        img_path = f"{job['user_id']}/{job['bucket_uuid']}/bg_removed_{job['category']}.png"
        
        await supabase.storage.from_(SUPABASE_TABLE).upload(
            file=bg_removed_image, 
            path=img_path,
            file_options={"cache-control": "3600", "upsert": "false"}
        )
        
        url_response = supabase.storage.from_(SUPABASE_TABLE).get_public_url(img_path)
        public_url = clean_url(url_response["publicURL"])
        
        await supabase.table(SUPABASE_TABLE).update({
            "removed_bg_image_url": public_url
        }).eq("job_id", job_id).execute()
        
        return public_url
    except Exception as e:
        print(f"Error in upload_bg_removed: {e}")
        return None
