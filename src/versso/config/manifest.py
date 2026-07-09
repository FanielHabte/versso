from pathlib import Path

import versso.util.helper as helper


def load_details() -> dict:
    root: Path = helper.project_root()
    manifest_path: Path = root / "src/versso/resources/main/manifest.json"

    if not manifest_path.exists():
        raise RuntimeError("Manifest file doesn't exist")

    return helper.fetch(manifest_path)
