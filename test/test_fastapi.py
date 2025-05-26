import requests
from PIL import Image
from io import BytesIO

# FastAPI uygulamanin çalıştığı adresi ve portu (örnek: localhost:8000)
url = "http://127.0.0.1:8000/process-image"

# Test resim yolu
test_image_path = "./images/beyaz-uzeri-serpme-tasli-tisort.jpeg"

with open(test_image_path, "rb") as img_file:
    files = {
        "photo": img_file,
        "clothing": img_file
    }
    resp = requests.post(url, files=files)

if resp.status_code == 200:
    img = Image.open(BytesIO(resp.content))
    img.show()
    print("Başarılı!")
else:
    print(f"Hata {resp.status_code}: {resp.text}")
