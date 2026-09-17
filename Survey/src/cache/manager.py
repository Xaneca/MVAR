import json
import hashlib
from pathlib import Path


CACHE_DIR = Path("cache")


def create_hash(config: dict) -> str:
    config_string = json.dumps(
        config,
        sort_keys=True
    )

    return hashlib.md5(
        config_string.encode()
    ).hexdigest()



def load_cache(cache_key, folder):
    if folder not in ("raw", "processed"):
        raise ValueError(
            "Invalid folder name. Must be 'raw' or 'processed'."
        )

    path = CACHE_DIR / f"{folder}" / f"{cache_key}.json"

    if not path.exists():
        return None

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_cache(cache_key, data, folder):
    if folder not in ("raw", "processed"):
        raise ValueError(
            "Invalid folder name. Must be 'raw' or 'processed'."
        )

    folder_path = CACHE_DIR / f"{folder}"

    folder_path.mkdir(
        exist_ok=True
    )

    path = folder_path / f"{cache_key}.json"

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )