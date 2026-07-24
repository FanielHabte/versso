from dataclasses import dataclass


@dataclass(frozen=True)
class AnalysisPayload:
    """
    An immutable data container holding identity metadata for an Amazon QuickSight Analysis.

    This payload acts as a structured contract used across factories and client modules
    to reference target AWS assets consistently.

    :cvar id: The unique operational identifier for the target QuickSight analysis.
    :cvar aws_account_id: The 12-digit numeric AWS Account ID where the resource resides.
    :cvar name: The display name or alias assigned to the analysis resource.
    """
    id: str
    aws_account_id: str
    name: str

    @classmethod
    def build_payload(cls, analysis_id: str, aws_account_id: str, client):
        kwargs = {
            "AwsAccountId": aws_account_id,
            "AnalysisId": analysis_id
        }
        response = client.describe_analysis(**kwargs)

        return AnalysisPayload(
            id=analysis_id,
            aws_account_id=aws_account_id,
            name=response["Name"]
        )
