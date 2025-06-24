from supabase import create_client, Client
from fastapi import UploadFile
from utils.image_utils import compress_image
from dotenv import load_dotenv
import uuid
import os

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL")  
SUPABASE_KEY: str = os.getenv("SUPABASE_ANON_KEY") 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

SUPABASE_TABLE = "wardrobe"

async def upload_supabase(user_id: str, clothe_image: UploadFile, category: str):
    try:
        byte_image = await clothe_image.read()
        #compressed_byte_image = compress_image(byte_image)
        bucket_uuid = str(uuid.uuid4())
        img_path = f"{user_id}/{bucket_uuid}/{category}.jpg"
        
        upload_response = supabase.storage.from_(SUPABASE_TABLE).upload(
            file=byte_image, 
            path=img_path,
            file_options={"cache-control": "3600", "upsert": "false"}
        )
        
        url_response = supabase.storage.from_(SUPABASE_TABLE).get_public_url(img_path)
        public_url = url_response[:-1]
        
        return public_url, bucket_uuid
    except Exception as e:
        print(f"Error in upload_supabase: {e}")
        return None

async def insert_supabase(img_url: str, user_id: str, category: str, is_long_top: bool):
    try:
        job_id = str(uuid.uuid4())
        
        response = supabase.table(SUPABASE_TABLE).insert({
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

async def upload_bg_removed(user_id: str, bucket_uuid: str, job_id: str, bg_removed_image: bytes, category: str):
    try:
        upload_response = supabase.storage.from_(SUPABASE_TABLE).upload(
            file=bg_removed_image, 
            path=f"{user_id}/{bucket_uuid}/bg_removed_{category}.png",
            file_options={"cache-control": "3600", "upsert": "false"}
        )
        
        img_path = upload_response.path
        url_response = supabase.storage.from_(SUPABASE_TABLE).get_public_url(img_path)
        public_url = url_response[:-1]
        
        update_response = supabase.table(SUPABASE_TABLE).update({
            "removed_bg_image_url": public_url
        }).eq("job_id", job_id).execute()
        
        return {"Status": "Finished"}
    except Exception as e:
        print(f"Error in upload_bg_removed: {e}")
        return None
