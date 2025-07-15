from typing import List, Dict

def extract_id(data: List[Dict]) -> str:
    """
    Tek bir kayıt içeren listeyi alır ve o kaydın 'id' alanını döner.
    Liste boşsa KeyError/IndexError fırlatır.
    """
    return data[0]["id"]
