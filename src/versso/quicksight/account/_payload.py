from dataclasses import dataclass


@dataclass(frozen=True)
class QuickSightAccountPayload:
    id: str
    name_space: str
