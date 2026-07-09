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


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent.parent


