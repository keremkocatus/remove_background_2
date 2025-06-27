import requests
import time
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://127.0.0.1:8000"
POLL_INTERVAL = 5  # saniye

def poll_job(job_id: str):
    url = f"{BASE_URL}/job-status/{job_id}"
    while True:
        resp = requests.post(url)
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
    ids = ['b9d669f8-1daf-4ab1-8665-0f30987542f5', '531c09a9-733e-473b-997d-ee258c412d5f', '1cc058ec-e800-4809-8731-c5bf05259325']
    main(ids)
