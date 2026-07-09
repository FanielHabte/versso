from pathlib import Path

from dataclasses import dataclass, fields
from versso.util.helper import fetch


@dataclass(frozen=True)
class Context:
    analysis: dict
    aws: dict
    dashboard: dict
    folder: dict
    project: dict
    user: dict
    team: dict

    @classmethod
    def load(cls):
        project_root: Path = Path(__file__).parent.parent.parent
        manifest_path: Path = project_root / "resources/main/manifest.json"

        config = fetch(manifest_path)

        context_data = {
            field.name: config[field.name]
            for field in fields(cls)
            if field.name in config
        }

        return cls(**context_data)
