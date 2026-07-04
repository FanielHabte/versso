from typing import Any

from versso.aws.quicksight.analysis.payload import AnalysisPayload
from pathlib import Path
from versso.util.helper import fetch
from versso.aws.quicksight.analysis.factory import build_prod_analysis_payload


def analysis_describe(analysis_payload: AnalysisPayload, quicksight_client) -> dict[str, Any]:
    """
    Pulls latest description of the given Analysis from the QuickSight API.

    :param quicksight_client:
    :param analysis_payload:
    :return: analysis_description
    """

    kwargs: dict[str, Any] = {
        "AwsAccountId": analysis_payload.aws_account_id,
        "AnalysisId": analysis_payload.analysis_id
    }

    if analysis_payload.version > 0:
        kwargs["Version"] = analysis_payload.version

    return quicksight_client.describe_analysis_definition(**kwargs)


def analysis_update(analysis_payload: AnalysisPayload,
                    analysis_description: dict[str, Any],
                    quicksight_client) -> dict[str, Any]:
    """
    Updated the given Analysis with the provided

    :param quicksight_client:
    :param analysis_payload:
    :param analysis_description:
    :return: response
    """

    update_response = quicksight_client.update_analysis(
        AwsAccountId=analysis_payload.aws_account_id,
        AnalysisId=analysis_payload.analysis_id,
        Name=analysis_payload.name,
        Definition=analysis_description["Definition"]
    )

    if update_response["UpdateStatus"] == "UPDATE_FAILED":
        error_message = update_response["Error"]["Message"]
        raise RuntimeError(f"Failed to update analysis due to {error_message}")

    return update_response


# def analysis_promote(beta: AnalysisPayload, prod: AnalysisPayload) -> dict[str, Any]:
#     beta_analysis_definition = analysis_describe(beta)
#     update_response = analysis_update(prod, beta_analysis_definition)
#
#     return update_response


def analysis_clone(original_analyses: AnalysisPayload,
                   project_name: str,
                   quicksight_client) -> dict[str, Any]:
    temp_create_response = analysis_create_template(project_name=project_name,
                                                    quick_client=quicksight_client)
    template = AnalysisPayload(analysis_id=temp_create_response["AnalysisId"],
                               aws_account_id="679432970382",
                               name=f"fani-{project_name}-analyses")

    original_analysis = analysis_describe(original_analyses, quicksight_client)
    update_response = analysis_update(template, original_analysis, quicksight_client)

    return update_response


def get_prod_analysis_payload() -> AnalysisPayload:
    return build_prod_analysis_payload()


## Helper Functions ##

def analysis_create_template(project_name: str, quick_client) -> dict[str, Any]:
    build_response = quick_client.create_analysis(**build_analyses_definition(project_name))

    return build_response


def build_analyses_definition(project_name):
    analyses_def = fetch(get_path("template_analyses"))
    # {team}-{project_name}-{user}
    analyses_def["AnalysisId"] = f"central-analytics-{project_name}-fani"
    # {user}-{project_name}-analyses
    analyses_def["Name"] = f"fani-{project_name}-analyses"

    return analyses_def


def get_path(file_name: str):
    root_path = Path(__file__).parent.parent.parent.parent
    file_path = root_path / f"resources/config/analyses/{file_name}.json"

    return file_path
