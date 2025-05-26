from PIL import Image
from io import BytesIO

async def compress_image(img: Image.Image,max_size: int = 1024,quality: int = 95):
    w, h = img.size
    
    if w<max_size and h<max_size:
        pass
    elif w>=h:
        scale = max_size / w
    else:
        scale = max_size / h
    
    img_resized = img.resize((int(scale*w), int(scale*h)), Image.Resampling.LANCZOS)
    
    buf = BytesIO()
    img_resized.save(buf,format="JPEG",quality=quality,optimize=True,progressive=True)
    buf.seek(0)
    
    return buf
    
    