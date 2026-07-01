from dataclasses import dataclass


@dataclass(frozen=True)
class AnalysisPayload:
    analysis_id: str
    aws_account_id: str
    name: str
    version: int = 0
