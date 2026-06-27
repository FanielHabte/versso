from dataclasses import dataclass


@dataclass()
class DashboardPayload:
    id: str
    account_id = str
    version: int = None
    version_set: bool = False


