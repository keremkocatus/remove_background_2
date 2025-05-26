from rembg import new_session, remove
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
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

# --- CORS Middleware Eklemesi ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # veya ["http://localhost:3000", "https://your-domain.com"]
    allow_credentials=True,
    allow_methods=["*"],            # GET, POST, PUT, DELETE, OPTIONS...
    allow_headers=["*"],            # Authorization, Content-Type, vs.
)
# -----------------------------------

@app.post("/process-image")
async def process_image(
    photo: UploadFile = File(...),
    clothing: UploadFile = File(...),
):
    contents = await photo.read()
    img = Image.open(BytesIO(contents))
    
    # Arka planı kaldır
    processed_image = remove(img, session=session)
    processed_image = processed_image.convert("RGB")
    processed_image.show()
    
    buf = BytesIO()
    processed_image.save(buf, format="JPEG")
    buf.seek(0)
    
    return StreamingResponse(buf, media_type="image/jpeg")

@app.post("/clothe-rembg")
async def clothe_rembg(clothing: UploadFile = File(...)):
    contents = await clothing.read()
    img = Image.open(BytesIO(contents))
    
    