from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from services.rembg_service import remove_background_rembg
from services.replicate_service import remove_background_replicate
from utils.image_utils import compress_image
from PIL import Image
from io import BytesIO

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

@router.post("/compress")
async def compress_image(file: UploadFile = File(...)):
    try:
        data = await file.read()
        img = Image.open(BytesIO(data))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image") from e
    
    buf = compress_image(img, max_size=1024, quality=85)

    return StreamingResponse(buf, media_type="image/jpeg")