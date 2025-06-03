import os
import replicate
import requests
from PIL import Image, ImageFilter
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()
REPL_TOKEN = os.getenv("REPLICATE_API_TOKEN")
_client = replicate.Client(api_token=REPL_TOKEN)

async def replicate_human_segmentation(img_url: str) -> bytes:
    try:
        output = _client.run(
            "schananas/grounded_sam:ee871c19efb1941f55f66a3d7d960428c8a5ab9ebc21c",
            input={
                "image": img_url,
                "mask_prompt": "human",
                "adjustment_factor": -15,
                "negative_mask_prompt": "",
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
        print(f"Error in replicate_human_segmentation: {e}")
        return None
