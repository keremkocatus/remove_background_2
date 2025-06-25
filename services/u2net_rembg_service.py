from rembg import new_session, remove
from fastapi import UploadFile
from PIL import Image
from io import BytesIO

_SESSION = new_session(model_name="u2net")

async def segment_human_from_background(photo: UploadFile):
    contents = await photo.read()
    img = Image.open(BytesIO(contents))
    processed = remove(img, session=_SESSION)

    return processed
