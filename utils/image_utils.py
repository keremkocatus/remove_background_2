from PIL import Image
from io import BytesIO

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

mask_prompt = {
    "top": "clothes",
    "longtop": "dress",
    "bottom": "pants",
    "one-piece": "clothes",
    "shoes": "shoes",
    "accessories": "accessories"
}

def get_mask_prompts(category: str, is_long_top: bool):
    try:
        negative_mask_prompt = ""
        
        if category == "top" and is_long_top:
            positive_mask_prompt = mask_prompt["longtop"]
        else:
            positive_mask_prompt = mask_prompt[category]
            
        return positive_mask_prompt, negative_mask_prompt
    except Exception as e:
        print(f"Error in get_mask_prompts: {e}")
        return None, None
