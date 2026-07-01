import json
from pathlib import Path
from versso.util.datetime_encoder import DateTimeEncoder
from typing import Any


def save(file_path: Path, json_response) -> Path:
    with open(file_path, "w") as file:
        json.dump(json_response, file, cls=DateTimeEncoder, indent=4)
        file.close()

    return file_path


def fetch(file_path: Path) -> dict[str, Any]:
    with open(file_path, "r") as file:
        json_data = json.load(file)
        file.close()

    return json_data


def get_project_root_path() -> Path:
    return Path(__file__).resolve().parent.parent.parent.parent


def get_manifest_file() -> dict[str, Any]:
    root_path = get_project_root_path()
    manifest_file_path = root_path / "src/versso/resources/main/manifest.json"

    return fetch(manifest_file_path)
