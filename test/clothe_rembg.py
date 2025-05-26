import replicate
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import requests

def load_api():
    load_dotenv()
    client = replicate.Client()

def clothe_remove_background(img_url,mask_prompt="clothe",negative_mask_prompt=""):    
    output = replicate.run(
        "schananas/grounded_sam:ee871c19efb1941f55f66a3d7d960428c8a5afcb77449547fe8e5a3ab9ebc21c",
        input={
            "image": img_url,
            "mask_prompt": mask_prompt,
            "adjustment_factor": -15,
            "negative_mask_prompt": negative_mask_prompt
        }
    )
    
    for i,item in enumerate(output):
        if i==2:
            mask_url = item

    resp = requests.get(mask_url)
    mask = Image.open(BytesIO(resp.content)).convert("L")
    
    resp = requests.get(img_url)
    img = Image.open(BytesIO(resp.content)).convert("RGBA")
    
    img = img.convert("RGBA")
    img.putalpha(mask)
    img.show()
    
    return img

def human_remove_background(img_url, mask_prompt="human", negative_mask_prompt=""):
    output = replicate.run(
        "schananas/grounded_sam:ee871c19efb1941f55f66a3d7d960428c8a5afcb77449547fe8e5a3ab9ebc21c",
        input={
            "image": img_url,
            "mask_prompt": mask_prompt,
            "adjustment_factor": -15,
            "negative_mask_prompt": negative_mask_prompt
        }
    )
    
    for i,item in enumerate(output):
        if i==2:
            mask_url = item

    resp = requests.get(mask_url)
    mask = Image.open(BytesIO(resp.content)).convert("L")
    
    resp = requests.get(img_url)
    img = Image.open(BytesIO(resp.content)).convert("RGBA")
    
    img.putalpha(mask)
    img.show()
    
    return img

load_api()

url="https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/try-on-images/c9000a73-0604-42f6-9f40-80addf8c0f66/try-on/a2280420-9b91-41c8-bf2f-8b0ce17b572d/input_clothing.jpg"
clothe_remove_background(url)