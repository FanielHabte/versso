from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LocalRepoPayload:
    """
    An immutable data container holding identity metadata for an Amazon QuickSight Analysis.

    This payload acts as a structured contract used across factories and client modules
    to reference target AWS assets consistently.

    :cvar name: The unique operational identifier for the target QuickSight analysis.
    :cvar description: The 12-digit numeric AWS Account ID where the resource resides.
    :cvar owner: The display name or alias assigned to the analysis resource.
    """
    name: str
    path: Path
