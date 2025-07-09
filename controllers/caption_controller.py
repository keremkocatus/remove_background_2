# controllers/caption_controller.py
# Extracted caption endpoint into its own router

from fastapi import APIRouter, HTTPException
from services.supabase_wardrobe_service import get_caption_of_image

# Create a dedicated router for image captioning
caption_router = APIRouter()

@caption_router.get("/caption")
async def generate_caption(image_url: str):
    """
    Generate or retrieve a caption for an image using ChatGPT

    Args:
        image_url: The URL of the image to get caption for

    Returns:
        Generated caption
    """
    try:
        caption = await get_caption_of_image(image_url)
        return {"image_url": image_url, "caption": caption}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating caption: {e}"
        )

# To integrate this controller, in your main application or router setup do:
#
# from fastapi import FastAPI
# from controllers.caption_controller import caption_router
#
# app = FastAPI()
# app.include_router(caption_router)
