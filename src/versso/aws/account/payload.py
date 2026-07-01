from dataclasses import dataclass


@dataclass(frozen=True)
class AwsAccountPayload:
    id: str
    alias: str
    region: str
