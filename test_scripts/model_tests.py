import replicate
from dotenv import load_dotenv
import os

load_dotenv()
replicate_api_token = os.getenv("REPLICATE_API_TOKEN")
replicate_client = replicate.Client(api_token=replicate_api_token)

input = {
    "image": "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/deneme/fc39d9f5-dfba-4f5f-bc73-f5638f8e6208/e88e92c9-d767-4e78-80fc-472ae386fff7/bottoms.jpg",
    "query": "clothe",
    "box_threshold": 0.2,
    "text_threshold": 0.2
}

output = replicate.run(
    "adirik/grounding-dino:efd10a8ddc57ea28773327e881ce95e20cc1d734c589f7dd01d2036921ed78aa",
    input=input
)
print(output)
#=> {"detections":[{"bbox":[19,204,408,563],"label":"pink mug...
