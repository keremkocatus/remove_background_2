import requests

url = "http://localhost:8000/wardrobe-remove-background"

user_id = "12345"
category = "shirt"
is_long_top = True  # bool tipi, formda "true"/"false" olarak gönderilmeli

image_path = "/images/beyaz-uzeri-serpme-tasli-tisort.jpeg"

def test_remove_background():
    with open(image_path, "rb") as img_file:
        files = {
            "clothe_image": (
                "clothe_image.jpg", 
                img_file, 
                "image/jpeg"
            )
        }
        data = {
            "user_id": user_id,
            "category": category,
            "is_long_top": is_long_top
        }

        resp = requests.post(url, files=files, data=data)
        try:
            resp.raise_for_status()
            print("Status Code:", resp.status_code)
            print("Response JSON:", resp.json())
        except requests.exceptions.HTTPError as e:
            print("Error:", e)
            print("Response Body:", resp.text)


