import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "http://localhost:8000/wardrobe-remove-background"
USER_ID = "fc39d9f5-dfba-4f5f-bc73-f5638f8e6208"
CATEGORY = "tops"
IS_LONG_TOP = False
IMAGE_PATH = "./images/green_sweat.jpg"

def start_job():
    with open(IMAGE_PATH, "rb") as img:
        files = {"clothe_image": img}
        # form verisi: tüm değerler string olarak gönderilmeli
        data = {
            "user_id": USER_ID,
            "category": CATEGORY,
            "is_long_top": str(IS_LONG_TOP).lower()
        }
        resp = requests.post(URL, data=data, files=files)
        resp.raise_for_status()
        job_id = resp.json()["job_id"]
        print(f"✅ Başlatıldı: {job_id}")
        return job_id

def main():
    # Aynı anda 3 paralel istek
    with ThreadPoolExecutor(max_workers=3) as exe:
        futures = [exe.submit(start_job) for _ in range(3)]
        job_ids = [f.result() for f in as_completed(futures)]

    print("\nTüm job_id’ler:", job_ids)
    return job_ids

if __name__ == "__main__":
    main()
