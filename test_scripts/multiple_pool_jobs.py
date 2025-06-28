import requests
import time
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://127.0.0.1:8000"
POLL_INTERVAL = 5  # saniye

def poll_job(job_id: str):
    url = f"{BASE_URL}/job-status/{job_id}"
    while True:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status")
        print(f"[{time.strftime('%X')}] Job {job_id} durumu: {status}")

        if status == "finished":
            print(f"✅ Job tamamlandı: {data.get('result_url')}")
            break
        elif status in ("failed", "canceled"):
            print(f"⚠️ Job {job_id} {status}")
            break
        time.sleep(POLL_INTERVAL)

def main(job_ids: list[str]):
    # Her job_id için paralel poll
    with ThreadPoolExecutor(max_workers=len(job_ids)) as exe:
        exe.map(poll_job, job_ids)

if __name__ == "__main__":
    # start_jobs.py’den aldığınız üç job_id’yi buraya geçirin:
    ids = ['7ed6855a-6e1f-4885-bd28-14445c9f7904', '4b775752-12e5-42ee-b55a-d4f561077bef', '821440fd-933c-4367-a2fd-31ddf07cbd14']
    main(ids)
