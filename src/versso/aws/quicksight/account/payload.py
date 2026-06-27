from dataclasses import dataclass

@dataclass()
class QuickSightAccountPayload:
    account_name: str
    edition: str
    name_space: str
    notification_email: str
