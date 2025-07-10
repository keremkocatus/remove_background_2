from typing import List, Dict

def extract_color_names_from_palette(palette: Dict[str, List[Dict[str, str]]]) -> List[str]:
    """
    Palette içindeki tüm renk adlarını düz liste olarak döner.
    """
    return [color["name"] for group in palette.values() for color in group]

def extract_materials(data: Dict) -> List[str]:
    """
    Material JSON'undan materyal isimlerini alır.
    """
    return data.get("materials", [])

def extract_styles(data: Dict) -> List[str]:
    """
    Style JSON'undan stil isimlerini alır.
    """
    return data.get("styles", [])
