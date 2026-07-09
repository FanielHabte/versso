from dataclasses import dataclass


@dataclass()
class FolderPayload:
    folder_id: str
    aws_account_id: str
    name: str
