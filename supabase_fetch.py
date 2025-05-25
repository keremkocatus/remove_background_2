from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Ortam değişkenlerini yükle (eğer .env kullanıyorsan)
load_dotenv()

# --- Supabase Ayarları ---
SUPABASE_URL: str = os.getenv("SUPABASE_URL")  
SUPABASE_KEY: str = os.getenv("SUPABASE_ANON_KEY") 
print(SUPABASE_KEY,SUPABASE_URL)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_try_ons():
    try:
        response = supabase.table("try_ons").select("*").execute()
        if response.data:
            print("Veriler çekildi:")
            for row in response.data:
                print(row)
        else:
            print("Hiç veri yok.")
    except Exception as e:
        print("Bir hata oluştu:", e)

# --- Kullanım ---
if __name__ == "__main__":
    fetch_try_ons()
