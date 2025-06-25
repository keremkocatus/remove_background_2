import os
import replicate
import requests
from PIL import Image, ImageFilter
from io import BytesIO
from utils.prompt_utils import get_mask_prompts
from dotenv import load_dotenv

load_dotenv()
REPL_TOKEN = os.getenv("REPLICATE_API_TOKEN")
_client = replicate.Client(api_token=REPL_TOKEN)

async def remove_background_replicate(img_url: str, category: str, is_long_top: bool) -> bytes:
    try:
        mask_prompt, negative_mask_prompt = get_mask_prompts(category, is_long_top)
        
        output = _client.run(
            "schananas/grounded_sam:ee871c19efb1941f55f66a3d7d960428c8a5ab9ebc21c",
            input={
                "image": img_url,
                "mask_prompt": mask_prompt,
                "adjustment_factor": -15,
                "negative_mask_prompt": negative_mask_prompt,
            },
        )
        
        for i, item in enumerate(output):
            if i == 2:
                mask_url = item

        resp = requests.get(mask_url)
        mask = Image.open(BytesIO(resp.content)).convert("L")

        resp2 = requests.get(img_url)
        img = Image.open(BytesIO(resp2.content)).convert("RGBA")
        img.putalpha(mask)
        
        r, g, b, alpha = img.split()
        alpha_smoothed = alpha.filter(ImageFilter.GaussianBlur(radius=1))
        img = Image.merge("RGBA", (r, g, b, alpha_smoothed))
        
        buf = BytesIO()
        img.save(buf, format="PNG", quality=85, optimize=True)
        
        return buf.getvalue()
    except Exception as e:
        print(f"Error in remove_background_replicate: {e}")
        return None
