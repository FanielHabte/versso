from dataclasses import dataclass


@dataclass(frozen=True)
class AnalysisPayload:
    """
    An immutable data container holding identity metadata for an Amazon QuickSight Analysis.

    This payload acts as a structured contract used across factories and client modules
    to reference target AWS assets consistently.

    :cvar analysis_id: The unique operational identifier for the target QuickSight analysis.
    :cvar aws_account_id: The 12-digit numeric AWS Account ID where the resource resides.
    :cvar name: The display name or alias assigned to the analysis resource.
    """
    analysis_id: str
    aws_account_id: str
    name: str
