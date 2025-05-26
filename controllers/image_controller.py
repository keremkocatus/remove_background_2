from fastapi import APIRouter, File, UploadFile, HTTPException
from services.rembg_service import remove_background_rembg
from services.replicate_service import remove_background_replicate

router = APIRouter()

@router.post("/process-image")
async def process_image(photo: UploadFile = File(...),clothing: UploadFile = File(...)):
    try:
        return await remove_background_rembg(photo, clothing)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clothe-rembg", response_model=dict)
async def clothe_rembg(image_url: str,mask_prompt: str = "clothe", negative_mask_prompt: str = ""):
    try:
        img = await remove_background_replicate(
            img_url=image_url,
            mask_prompt=mask_prompt,
            negative_mask_prompt=negative_mask_prompt,
        )
        return {"message": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
