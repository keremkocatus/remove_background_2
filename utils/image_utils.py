from PIL import Image, ImageFilter
from io import BytesIO
import requests

# Fetch mask and apply it to the image
def process_mask(mask_url: str, job: dict[str, str]) -> bytes:
    try:
        resp = requests.get(mask_url)
        mask = Image.open(BytesIO(resp.content)).convert("L")

        resp2 = requests.get(job["image_url"])
        img = Image.open(BytesIO(resp2.content)).convert("RGBA")
        img.putalpha(mask)
        
        r, g, b, alpha = img.split()
        alpha_smoothed = alpha.filter(ImageFilter.GaussianBlur(radius=1))
        img = Image.merge("RGBA", (r, g, b, alpha_smoothed))
        
        buf = BytesIO()
        img.save(buf, format="PNG", quality=90, optimize=True)
        
        return buf.getvalue()
    except Exception as e:
        print(f"Error in process_mask: {e}")
        raise

def get_image_from_url(url: str):
    try:
        resp = requests.get(url)
        img = Image.open(BytesIO(resp.content))

        buf = BytesIO()
        img.save(buf, format="PNG", quality=90, optimize=True)

        return buf.getvalue()
    except Exception as e:
        print(f"Error in get_image_from_url: {e}")
        raise
# Resize and save image as JPEG
def compress_image(img: bytes, max_size: int = 1024, quality: int = 85):
    try:
        img_file = Image.open(BytesIO(img))
        
        if img_file.mode in ("RGBA", "P"):
            img_file = img_file.convert("RGB")
            
        w, h = img_file.size
        
        if w <= max_size and h <= max_size:
            scale = 1.0
        elif w >= h:
            scale = max_size / w
        else:
            scale = max_size / h
        
        if scale < 1.0:
            img_resized = img_file.resize(
                (int(scale * w), int(scale * h)), 
                Image.Resampling.LANCZOS
            )
        else:
            img_resized = img_file
        
        buf = BytesIO()
        img_resized.save(
            buf, 
            format="JPEG", 
            quality=quality, 
            optimize=True, 
            progressive=True
        )
        
        return buf.getvalue()
    except Exception as e:
        print(f"Error in compress_image: {e}")
        return None
