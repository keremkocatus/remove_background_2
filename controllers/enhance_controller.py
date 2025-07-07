from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Request

router = APIRouter()

@router.post("/enhance-image")
async def enhance_image(user_id: str = Form(...), clothe_image: UploadFile = File(...)):
    
    pass