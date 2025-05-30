from supabase import create_client, Client
from fastapi import UploadFile
from dotenv import load_dotenv
import uuid
import os

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL")  
SUPABASE_KEY: str = os.getenv("SUPABASE_ANON_KEY") 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def upload_supabase(user_id: str, clothe_image: UploadFile, category: str):
    
    byte_image = await clothe_image.read()
    bucket_uuid = str(uuid.uuid4())
    
    upload_response = supabase.storage.from_("wardrobe").upload(file=byte_image, 
                                                                path=f"{user_id}/{bucket_uuid}/{category}.jpg",
                                                                file_options={"cache-control": "3600", "upsert": "false"})
    
    img_path = upload_response.path
    url_response = supabase.storage.from_("wardrobe").get_public_url(img_path)
    public_url = url_response[:-1]
    
    return public_url, bucket_uuid
    
async def insert_supabase(img_url: str, user_id: str, category: str, islongtop: bool):
    
    job_id = str(uuid.uuid4())
    
    response = supabase.table("wardrobe").insert({"image_url": img_url,
                                                  "user_id": user_id,
                                                  "category": category,
                                                  "is_long_top": islongtop,
                                                  "job_id": job_id}).execute()
    
    return job_id

async def upload_bg_removed(user_id: str, bucket_uuid: str, job_id: str, bg_removed_image: bytes, category: str):
    
    upload_response = supabase.storage.from_("wardrobe").upload(file=bg_removed_image, 
                                                        path=f"{user_id}/{bucket_uuid}/bg_removed_{category}.png",
                                                        file_options={"cache-control": "3600", "upsert": "false"})
    
    img_path = upload_response.path
    url_response = supabase.storage.from_("wardrobe").get_public_url(img_path)
    public_url = url_response[:-1]
    
    update_response = supabase.table("wardrobe").update({"removed_bg_image_url": public_url}).eq("job_id", job_id).execute()
    
    return {"Status": "Finished"}