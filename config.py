import requests

# 1) Endpoint URL
url = "http://localhost:8000/wardrobe-remove-background"

# 2) UUID'yi stringe çevir
user_id   = "f6be7181-5cce-4a50-ba89-0f9f8eac8a9f"
category  = "top"
is_long_top = False

# 3) Dosya
files = {
    "clothe_image": open("./images/toptest.jpg", "rb")
}

# 4) Form verisi (string-boolean)
data = {
    "user_id":   user_id,           # ← zaten string
    "category":  category,
    "is_long_top": is_long_top
}

# 5) POST
resp = requests.post(url, data=data, files=files)

print("Status code:", resp.status_code)
print("Response body:", resp.text)
