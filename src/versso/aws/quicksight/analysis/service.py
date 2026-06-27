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

    return quick_client.describe_analysis_definition(**kwargs)


def update(analysis_payload: AnalysisPayload, analysis_description: dict[str, Any]) -> dict[str, Any]:
    """
    Updated the given Analysis with the provided

    :param analysis_payload:
    :param analysis_description:
    :return: response
    """

    response = quick_client.update_analysis(
        AwsAccountId=analysis_payload.aws_account_id,
        AnalysisId=analysis_payload.id,
        Name=analysis_payload.name,
        Definition=analysis_description["Definition"]
    )

    if response["UpdateStatus"] == "UPDATE_FAILED":
        error_message = response["Error"]["Message"]
        raise RuntimeError(f"Failed to update analysis due to {error_message}")

    return response


def promote(beta: AnalysisPayload, prod: AnalysisPayload) -> dict[str, Any]:
    beta_analysis_definition = pull(beta)
    update_response = update(prod, beta_analysis_definition)

    return update_response
