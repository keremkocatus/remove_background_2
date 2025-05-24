from rembg import new_session, remove
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from PIL import Image
from io import BytesIO

session = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global session
    session = new_session(model_name="u2net")
    yield
    
app = FastAPI(lifespan=lifespan)

@app.post("/process-image")
async def process_image(
    photo: UploadFile = File(...),
    clothing: UploadFile = File(...),
):
    
    contents = await photo.read()
    img = Image.open(BytesIO(contents))
    
    processed_image = remove(img, session=session)
    processed_image = processed_image.convert("RGB")
    
    buf = BytesIO()
    processed_image.save(buf, format="jpeg")
    buf.seek(0)
    
    return StreamingResponse(buf, media_type="image/jpeg")

    
    
