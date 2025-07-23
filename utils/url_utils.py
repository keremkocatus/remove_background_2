import re

def clean_url(response_url: str):
    if response_url.endswith("?"):
        return response_url[:-1]
    return response_url

def extract_bucket_id(image_url: str) -> str:
    """
    Supabase image_url'den UUID olan klasör adını çıkarır.
    Örnek URL:
    https://.../public/deneme/<user_id>/<bucket_id>/<filename>.jpg
    """
    cleaned_url = clean_url(image_url)

    # Regex ile UUID (bucket id) yakala
    match = re.search(r"/([0-9a-fA-F\-]{36})/", cleaned_url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Bucket ID (UUID) not found in the URL.")
