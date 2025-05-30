from PIL import Image
from io import BytesIO

def compress_image(img: Image.Image, max_size: int = 1024, quality: int = 95):
    w, h = img.size
    
    if w<max_size and h<max_size:
        pass
    elif w>=h:
        scale = max_size / w
    else:
        scale = max_size / h
    
    img_resized = img.resize((int(scale*w), int(scale*h)), Image.Resampling.LANCZOS)
    
    buf = BytesIO()
    img_resized.save(buf, format="JPEG", quality=quality, optimize=True, progressive=True)
    buf.seek(0)
    
    return buf

def prompt_generator(category: str, islongtop: bool):
    
    if category=="top" and islongtop:
        mask_prompt = "clothes,dress"
        negative_mask_prompt = "pants,skirts,shorts,shoes"
    elif category=="top":
        mask_prompt = "clothes"
        negative_mask_prompt = "pants,skirts,shorts,shoes"
    elif category=="bottom":
        mask_prompt = "clothes,pants,shorts,skirts"
        negative_mask_prompt = "tshirts,sweats,dresses,shoes"
    elif category=="one-piece":
        mask_prompt = "clothes"
        negative_mask_prompt = "shoes"
    elif category=="shoes":
        mask_prompt = "shoes"
        negative_mask_prompt = "clothes"
    elif category=="accessories":
        mask_prompt = "accessories"
        negative_mask_prompt = "clothes,shoes"
        
    return mask_prompt, negative_mask_prompt