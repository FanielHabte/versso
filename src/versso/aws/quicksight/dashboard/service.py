from typing import Any

from payload import DashboardPayload
from pathlib import Path
from versso.util.helper import fetch
from time import sleep


def dashboard_describe(dashboard_payload: DashboardPayload,
                       quicksight_client) -> dict[str, Any]:
    """
    Pulls latest description of the given dashboard from the QuickSight API.

    :param quicksight_client:
    :param dashboard_payload:
    :return: dashboard_description
    """

    kwargs: dict[str, Any] = {
        "AwsAccountId": dashboard_payload.aws_account_id,
        "DashboardId": dashboard_payload.id
    }

    if dashboard_payload.version_set:
        kwargs["VersionNumber"] = dashboard_payload.version

    return quicksight_client.describe_dashboard_definition(**kwargs)


def dashboard_update(dashboard_payload: DashboardPayload,
                     dashboard_description: dict[str, Any],
                     quicksight_client) -> dict[str, Any]:
    """
    Updated the given dashboard with the provided

    :param quicksight_client:
    :param dashboard_payload:
    :param dashboard_description:
    :return: response
    """

    update_response = quicksight_client.update_dashboard(
        AwsAccountId=dashboard_payload.aws_account_id,
        DashboardId=dashboard_payload.id,
        Name=dashboard_payload.name,
        Definition=dashboard_description["Definition"]
    )
    dashboard_payload.version = int(str(update_response["VersionArn"]).rsplit("/")[-1])
    dashboard_payload.version_set = True

    while True:

        describe_response = quicksight_client.describe_dashboard(
            AwsAccountId=dashboard_payload.aws_account_id,
            DashboardId=dashboard_payload.id,
            VersionNumber=dashboard_payload.version
        )

        status = describe_response["Dashboard"]["Version"]["Status"]
        print(f"Current Update Status: {status}")

        if status in ["CREATION_SUCCESSFUL", "UPDATE_SUCCESSFUL"]:
            return update_response

        if status in ["CREATION_FAILED", "UPDATE_FAILED"]:
            errors = describe_response["Dashboard"]["Version"].get("Errors", "Check DataSetArn permissions.")
            raise RuntimeError(f"QuickSight failed to compile layout: {errors}")

        sleep(5)


# def dashboard_promote(beta: dashboardPayload, prod: dashboardPayload) -> dict[str, Any]:
#     beta_dashboard_definition = dashboard_describe(beta)
#     update_response = dashboard_update(prod, beta_dashboard_definition)
#
#     return update_response


def dashboard_clone(original_dashboard: DashboardPayload,
                    project_name: str,
                    quicksight_client) -> dict[str, Any]:
    temp_create_response = dashboard_create_template(project_name=project_name)
    template_dashboard = build_template_dashboard(temp_create_response["DashboardId"],
                                                  original_dashboard.aws_account_id, project_name)

    original_dashboard = dashboard_describe(original_dashboard, quicksight_client)
    update_response = dashboard_update(template_dashboard, original_dashboard, quicksight_client)

    new_dashboard_version = int(str(update_response["VersionArn"]).rsplit("/")[-1])
    publish_response = dashboard_publish(dashboard_payload=template_dashboard, version_number=new_dashboard_version,
                                         quicksight_client=quicksight_client)

    return publish_response


def dashboard_publish(dashboard_payload: DashboardPayload,
                      version_number: int,
                      quicksight_client) -> dict[str, Any]:
    """
    Programmatically promotes a specific version number to be the active,
    live-facing production dashboard view.
    """
    return quicksight_client.update_dashboard_published_version(
        AwsAccountId=dashboard_payload.aws_account_id,
        DashboardId=dashboard_payload.id,
        VersionNumber=version_number
    )


## Helper Functions ##

def build_template_dashboard(dashboard_id, aws_account_id, project_name):
    return DashboardPayload(dashboard_id=dashboard_id, aws_account_id=aws_account_id,
                            name=f"fani-{project_name}-dashboard")


def dashboard_create_template(project_name: str) -> dict[str, Any]:
    build_response = quick_client.create_dashboard(**build_dashboard_definition(project_name))

    return build_response


def build_dashboard_definition(project_name):
    dashboard_def = fetch(get_path("template_dashboard"))
    # {team}-{project_name}-{user}
    dashboard_def["DashboardId"] = f"central-analytics-{project_name}-dev-fani-dashboard"
    # {user}-{project_name}-dashboard
    dashboard_def["Name"] = f"fani-{project_name}-dashboard"

    return dashboard_def


def get_path(file_name: str):
    root_path = Path("/Users/fanielhabte/PycharmProjects/versso")
    file_path = root_path / f"src/versso/resources/config/dashboard/{file_name}.json"

    return file_path


if __name__ == "__main__":
    from versso.aws.quicksight.account.service import get_qs_client_from_session

    my_project_name = "web-analytics"
    aws_account = "679432970382"
    quick_client = get_qs_client_from_session("us-east-1", "default")
    prod_dashboard = DashboardPayload(dashboard_id="1de66629-bd1f-4568-a8fc-49aec0d37608",
                                      aws_account_id=aws_account,
                                      name="web-analytics-dashboard-prod")
    template_dashboard = DashboardPayload(dashboard_id="central-analytics-web-analytics-dev-fani-dashboard",
                                          aws_account_id=aws_account,
                                          name="web-analytics-dashboard-prod")

    response = dashboard_clone(original_dashboard=prod_dashboard,
                               project_name=my_project_name,
                               quicksight_client=quick_client)

    print(response)
