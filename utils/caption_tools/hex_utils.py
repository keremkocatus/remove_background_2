import pathlib
import json

# Load color mappings from constants
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
with open(BASE_DIR / "constants" / "clothe_color.json", "r") as f:
    COLOR_DATA = json.load(f)

# Create a flat mapping of color name -> hex
COLOR_NAME_TO_HEX = {}
for palette in COLOR_DATA["color_palettes"].values():
    for color in palette:
        COLOR_NAME_TO_HEX[color["name"]] = color["hex"]   


def convert_colors_to_hex_format(color_names: list[str]) -> list[dict]:
    """Convert color names to [{name, hex}] format"""
    result = []
    for name in color_names:
        hex_code = COLOR_NAME_TO_HEX.get(name, "#000000")  # default to black
        result.append({"name": name, "hex": hex_code})
    return result