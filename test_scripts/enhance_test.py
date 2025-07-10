# test_enhance_image.py

import requests

def test_enhance_image():
    # Change this to wherever your FastAPI app is running
    base_url = "http://localhost:8000"
    endpoint = f"{base_url}/enhance-image"

    # Replace with your actual test values
    payload = {
        "user_id": "fc39d9f5-dfba-4f5f-bc73-f5638f8e6208",
        "bucket_id": "efa5f4e9-87a6-43b4-91ce-cbe9b6dddd75",
        "clothe_image_url": "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/deneme/fc39d9f5-dfba-4f5f-bc73-f5638f8e6208/efa5f4e9-87a6-43b4-91ce-cbe9b6dddd75/bg_removed_bottoms.png"
    }

    try:
        resp = requests.post(endpoint, data=payload)
        resp.raise_for_status()
        data = resp.json()
        print("Success:", data)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err} - Response: {resp.text}")
    except Exception as err:
        print(f"Other error: {err}")

if __name__ == "__main__":
    test_enhance_image()
