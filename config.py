import requests
import uuid

# 1) Endpoint URL
url = "http://localhost:8000/wardrobe-remove-background"

# 2) UUID'yi stringe çevir
user_id   = "e94961f4-d5d9-4b1e-b85a-9e6e693fa67f"
category  = "top"
islongtop = True

# 3) Dosya
files = {
    "clothe_image": open("./images/beyaz-uzeri-serpme-tasli-tisort.jpeg", "rb")
}

# 4) Form verisi (string-boolean)
data = {
    "user_id":   user_id,           # ← zaten string
    "category":  category,
    "islongtop": False
}

# 5) POST
resp = requests.post(url, data=data, files=files)

print("Status code:", resp.status_code)
print("Response body:", resp.text)
