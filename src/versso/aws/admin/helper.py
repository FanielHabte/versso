import json
from pathlib import Path
from datetime import datetime
from typing import Any


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


def save(file_path: Path, json_response) -> Path:
    with open(file_path, "w") as file:
        json.dump(json_response, file, cls=DateTimeEncoder, indent=4)
        file.close()

    return file_path


def fetch(file_path: Path) -> dict[str, Any]:
    with open("initial_pull.json", "r") as file:
        json_data = json.load(file)
        file.close()

    return json_data
