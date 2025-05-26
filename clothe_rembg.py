import replicate
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO,BufferedReader
import requests

def load_api():
    load_dotenv()
    client = replicate.Client()

def clothe_remove_background(img,mask_prompt="human",negative_mask_prompt=""):
    img = image2filelike(img)
    
    output = replicate.run(
        "schananas/grounded_sam:ee871c19efb1941f55f66a3d7d960428c8a5afcb77449547fe8e5a3ab9ebc21c",
        input={
            "image": img,
            "mask_prompt": mask_prompt,
            "adjustment_factor": -15,
            "negative_mask_prompt": negative_mask_prompt
        }
    )
    
    for i,item in enumerate(output):
        if i==2:
            mask_url = item
            #print(item)   

    resp = requests.get(mask_url)
    mask = Image.open(BytesIO(resp.content)).convert("L")
    
    img = filelike2image(img)
    img = img.convert("RGBA")
    img.putalpha(mask)
    img.show()
    
    return img

def image2filelike(img):
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    
    return BufferedReader(buffer)

def filelike2image(filelike):
    filelike.seek(0)
    img = Image.open(BytesIO(filelike.read()))
    img.load()
    
    return img

load_api()

img_path = "./images/peder.jpg" 
img = Image.open(img_path)

clothe_remove_background(img)