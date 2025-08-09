import os
from dotenv import load_dotenv
from core import routes

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY       = os.getenv("OPENAI_API_KEY")
REPLICATE_API_KEY    = os.getenv("REPLICATE_API_TOKEN")

# Supabase Config
SUPABASE_URL         = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY    = os.getenv("SUPABASE_ANON_KEY")

# Tables & Buckets
REVIEW_TABLE         = os.getenv("REVIEW_TABLE")
WARDROBE_BUCKET_NAME = os.getenv("WARDROBE_BUCKET_NAME")
CLOTHES_DETAIL_TABLE = os.getenv("CLOTHES_DETAIL_TABLE")
EDIT_BUCKET_NAME     = os.getenv("EDIT_BUCKET_NAME")
EDIT_TABLE_NAME      = os.getenv("EDIT_TABLE_NAME")
ERROR_LOG_TABLE      = os.getenv("ERROR_LOG_TABLE")
REVIEW_BUCKET        = os.getenv("REVIEW_BUCKET")

# Webhooks & Model IDs
EDIT_WEBHOOK_URL     = f"{os.getenv('REPLICATE_WEBHOOK_URL')}{routes.WEBHOOK_IMAGE_EDIT}"
ENHANCE_MODEL_ID     = os.getenv("ENHANCE_MODEL_ID")
ENHANCE_WEBHOOK_URL  = f"{os.getenv('REPLICATE_WEBHOOK_URL')}{routes.WEBHOOK_ENHANCE}"
LATE_ENHANCE_WEBHOOK_URL  = f"{os.getenv('REPLICATE_WEBHOOK_URL')}{routes.WEBHOOK_LATE_ENHANCE}"
FAST_MODEL_ID        = os.getenv("FAST_MODEL_ID")
REMBG_WEBHOOK_URL    = f"{os.getenv('REPLICATE_WEBHOOK_URL')}{routes.WEBHOOK_FAST_REMBG}"
