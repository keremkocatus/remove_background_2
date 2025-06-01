import os
import replicate
import requests
from PIL import Image
from io import BytesIO
from utils.image_utils import prompt_generator
from dotenv import load_dotenv

load_dotenv()
REPL_TOKEN = os.getenv("REPLICATE_API_TOKEN")
_client = replicate.Client(api_token=REPL_TOKEN)

async def remove_background_replicate(img_url: str, category: str, is_long_top: bool) -> bytes:
    
    mask_prompt, negative_mask_prompt = prompt_generator(category, is_long_top)
    
    output = _client.run(
        "schananas/grounded_sam:ee871c19efb1941f55f66a3d7d960428c8a5afcb77449547fe8e5a3ab9ebc21c",
        input={
            "image": img_url,
            "mask_prompt": mask_prompt,
            "adjustment_factor": -15,
            "negative_mask_prompt": negative_mask_prompt,
        },
    )
    
    for i,item in enumerate(output):
        if i==2:
            mask_url = item

    resp = requests.get(mask_url)
    mask = Image.open(BytesIO(resp.content)).convert("L")

    resp2 = requests.get(img_url)
    img = Image.open(BytesIO(resp2.content)).convert("RGBA")
    img.putalpha(mask)
    
    buf = BytesIO()
    img.save(buf, format="PNG", quality=80, optimize=True)
    
    return buf.getvalue()
