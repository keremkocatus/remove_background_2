import requests

# 1) Endpoint URL
url = "http://localhost:8000/wardrobe-remove-background"

# 2) UUID'yi stringe çevir
user_id   = "fc39d9f5-dfba-4f5f-bc73-f5638f8e6208"
category  = "top"
is_long_top = False

# 3) Dosya
files = {
    "clothe_image": open("./images/green_sweat.jpg", "rb")
}

# 4) Form verisi (string-boolean)
data = {
    "user_id":   user_id,           
    "category":  category,
    "is_long_top": is_long_top
}

# 5) POST
resp = requests.post(url, data=data, files=files)

print("Status code:", resp.status_code)
print("Response body:", resp.text)

