import json
from pathlib import Path
from types import SimpleNamespace

def load_routes(json_path: str = "routes.json") -> SimpleNamespace:
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"Route config file not found: {json_path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    def to_namespace(obj):
        if isinstance(obj, dict):
            return SimpleNamespace(**{k: to_namespace(v) for k, v in obj.items()})
        return obj

    return to_namespace(data)
