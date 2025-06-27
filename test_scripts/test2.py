import requests
import time

BASE_URL = "http://127.0.0.1:8000"  
POLL_INTERVAL = 5  

def poll_job_status(job_id: str):
    url = f"{BASE_URL}/job-status/{job_id}"
    while True:
        resp = requests.post(url)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            print(f"HTTP error: {e}")
            break

        data = resp.json()
        status = data.get("status")
        print(f"[{time.strftime('%X')}] Job {job_id} status: {status}")

        if status == "finished":
            print("✅ Job tamamlandı. Sonuç URL:", data.get("result_url"))
            break
        elif status in ("failed", "canceled"):
            print(f"⚠️ Job {status}.")
            break
        else:
            time.sleep(POLL_INTERVAL)

job_id = "e142673c-41d7-489e-a0df-8b3556721c38" 
poll_job_status(job_id)
