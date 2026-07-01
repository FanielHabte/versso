from typing import Any

from versso.aws.quicksight.dataset.payload import DatasetPayload


def dataset_describe(account_id: str, dataset_id: str):
    analysis_description = quick_client.describe_dashboard(AwsAccountId=account_id, DataSetId=dataset_id)

    return analysis_description


def dataset_update(dataset_payload: DatasetPayload, dataset_description: dict[str, Any]) -> dict[str, Any]:
    """
    Updated the given Analysis with the provided

    :param dataset_payload:
    :param dataset_description:
    :return: response
    """

    response = quick_client.update_analysis(
        AwsAccountId=dataset_payload.aws_account_id,
        AnalysisId=dataset_payload.id,
        Name=dataset_payload.name,
        Definition=dataset_description["Definition"]
    )

    if response["UpdateStatus"] == "UPDATE_FAILED":
        error_message = response["Error"]["Message"]
        raise RuntimeError(f"Failed to update analysis due to {error_message}")

    return response


def dataset_clone(beta: DatasetPayload, prod: DatasetPayload) -> dict[str, Any]:
    beta_analysis_definition = dataset_describe(beta)
    update_response = dashboard_push(prod, beta_analysis_definition)

    return update_response


if __name__ == "__main__":
    from versso.aws.quicksight.account.service import get_qs_client_from_session

    quick_client = get_qs_client_from_session(profile_name="default", region="us-east-1")