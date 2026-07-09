from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetPayload:
    dataset_id: str
    account_id = str
