from git import Repo
from pathlib import Path

from versso.git.remote.template.payload import TemplatePayload


class RemoteTemplate:

    def __init__(self, template_payload: TemplatePayload, local_path: Path):
        self.payload = template_payload
        self.local_path = local_path

    def clone(self) -> None:
        if not self.local_path.exists():
            raise RuntimeError(f"path {self.local_path} is not a valid path")
        Repo.clone_from(self.payload.git_address, self.local_path)
