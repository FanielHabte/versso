import json
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class FolderPayload:
    id: str
    aws_account_id: str
    name: str


