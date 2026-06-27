from typing import Any

from versso.aws.admin import client
from .payload import AnalysisPayload

quick_client = client.build("us-east-1", "default")


def pull(analysis_payload: AnalysisPayload) -> dict[str, Any]:
    """
    Pulls latest description of the given Analysis from the QuickSight API.

    :param analysis_payload:
    :return: analysis_description
    """

    kwargs: dict[str, Any] = {
        "AwsAccountId": analysis_payload.aws_account_id,
        "AnalysisId": analysis_payload.id
    }

    if analysis_payload.version_set:
        kwargs["VersionNUMBER"] = analysis_payload.version

    return quick_client.describe_analysis(**kwargs)


def update(analysis_description: dict[str, Any]) -> dict[str, Any]:
    """
    Updated the given Analysis with the provided
    :param analysis_description:
    :return: response
    """

    response = quick_client.update_analysis(analysis_description)

    if response["status"] == 200:
        return response
    else:
        error_message = response["Error"]["Message"]
        raise RuntimeError(f"Failed to update analysis due to {error_message}")
