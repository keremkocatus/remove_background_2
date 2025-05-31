from PIL import Image
from io import BytesIO

def compress_image(img: bytes, max_size: int = 1024, quality: int = 75):
    img_file = Image.open(BytesIO(img))
    
    if img_file.mode in ("RGBA", "P"):
        img_file = img_file.convert("RGB")
        
    w, h = img_file.size
    
    if w<=max_size and h<=max_size:
        scale = 1.0
    elif w>=h:
        scale = max_size / w
    else:
        scale = max_size / h
    
    if scale < 1.0:
        img_resized = img_file.resize((int(scale*w), int(scale*h)), Image.Resampling.LANCZOS)
    else:
        img_resized = img_file
    
    buf = BytesIO()
    img_resized.save(buf, format="JPEG", quality=quality, optimize=True, progressive=True)
    
    return buf.getvalue()

def prompt_generator(category: str, islongtop: bool):
    
    if category=="top" and islongtop:
        mask_prompt = "dress"
        negative_mask_prompt = ""
    elif category=="top":
        mask_prompt = "clothes"
        negative_mask_prompt = ""
    elif category=="bottom":
        mask_prompt = "pants"
        negative_mask_prompt = ""
    elif category=="one-piece":
        mask_prompt = "clothes"
        negative_mask_prompt = ""
    elif category=="shoes":
        mask_prompt = "shoes"
        negative_mask_prompt = ""
    elif category=="accessories":
        mask_prompt = "accessories"
        negative_mask_prompt = ""
        
    return mask_prompt, negative_mask_prompt