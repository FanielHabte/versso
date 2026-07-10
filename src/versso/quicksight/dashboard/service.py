from versso.quicksight.dashboard.payload import DashboardPayload as _DashboardPayload
from versso.quicksight.interfaces.i_service import Service
from versso.quicksight.setup.context import Context as _Context
from pathlib import Path as _Path
from versso.util.helper import fetch as _fetch
from time import sleep as _sleep


class Dashboard(Service):
    """
    Encapsulates Amazon QuickSight Dashboard operations.

    Provides a clean interface to create, define, describe, update, clone, and promote
    QuickSight dashboard utilizing an underlying QuickSight client and structural payloads.
    """

    def __init__(self, context: _Context, dashboard_payload: _DashboardPayload, quicksight_client):
        """
        Initializes the Dashboard instance.

        Args:
            dashboard_payload (_DashboardPayload): Data object containing the dashboard metadata.
            quicksight_client: The initialized AWS QuickSight boto3 client.
        """
        super().__init__(context=context, client=quicksight_client, payload=dashboard_payload)
        self.version = 0

    def create(self):
        pass

    def define(self) -> dict:
        """
        Pulls the latest definition of the given Dashboard from the QuickSight API.

        :return: The dashboard definition structure.
        """
        kwargs: dict = {
            "AwsAccountId": self.payload.aws_account_id,
            "DashboardId": self.payload.dashboard_id
        }

        if self.version > 0:
            kwargs["VersionNumber"] = self.version

        return self.client.describe_dashboard_definition(**kwargs)["Definition"]

    def describe(self) -> dict:
        """
        Retrieves top-level metadata and configuration for the dashboard.

        :return: A dictionary representing the AWS API response from describe_dashboard.
        """
        kwargs: dict = {
            "AwsAccountId": self.payload.aws_account_id,
            "DashboardId": self.payload.dashboard_id
        }
        return self.client.describe_dashboard(**kwargs)

    def update(self, definition: dict) -> dict:
        """
        Updates the given dashboard with the provided layout definition and blocks
        until the QuickSight deployment job completes successfully.

        Args:
            definition (dict): The target layout/data definition schema.

        Raises:
            RuntimeError: If the QuickSight compilation fails or errors occur during deployment.

        Returns:
            (dict): The original update API response payload.
        """
        kwargs: dict = {
            "AwsAccountId": self.client.aws_account_id,
            "DashboardId": self.client.dashboard_id,
            "Name": self.client.name,
            "Definition": definition
        }

        update_response = self.client.update_dashboard(**kwargs)

        self.version = int(str(update_response["VersionArn"]).rsplit("/")[-1])

        while True:
            describe_response = self.describe()["Dashboard"]
            status = describe_response["Version"]["Status"]

            if status in ["CREATION_SUCCESSFUL", "UPDATE_SUCCESSFUL"]:
                return update_response

            if status in ["CREATION_FAILED", "UPDATE_FAILED"]:
                errors = describe_response["Dashboard"]["Version"].get("Errors", "Check DataSetArn permissions.")
                raise RuntimeError(f"QuickSight failed to compile layout: {errors}")

            _sleep(5)

    def promote_to(self, target: "Dashboard") -> "Dashboard":
        """
        Pushes the current dashboard's source definition to a target dashboard
        and automatically publishes it live.

        Args:
            target (Dashboard): The downstream dashboard instance receiving the deployment.

        Returns:
            Dashboard: The updated and published target dashboard instance.
        """
        target.update(self.define())
        target.publish()

        return target

    def clone(self) -> "Dashboard":
        """
        Creates an isolated developer remote workspace, copies the current
        dashboard's definition layout into it, and publishes it live.

        Returns:
            Dashboard: A fresh, newly created dashboard workspace clone.
        """
        template_dashboard = self._create_template()

        copy: "Dashboard" = Dashboard(
            context=self.context,
            dashboard_payload=template_dashboard,
            quicksight_client=self.client
        )

        copy.update(self.define())
        copy.publish()

        return copy

    def publish(self) -> dict:
        """
        Programmatically promotes a specific version number to be the active,
        live-facing production dashboard view.

        Returns:
            dict: The API response payload from the published version change request.
        """
        return self.client.update_dashboard_published_version(
            AwsAccountId=self.client.aws_account_id,
            DashboardId=self.client.dashboard_id,
            VersionNumber=self.version
        )

    def _create_template(self) -> _DashboardPayload:
        """
        Generates a development workspace remote container via QuickSight API
        using local configuration context files.

        Returns:
            _DashboardPayload: The payload metadata for the newly instantiated remote dashboard.
        """

        template_definition: dict = _build_template_definition(
            project_name=self.context.project["name"],
            user_name=self.context.user["alias"],
            team_name=self.context.team["name"]
        )
        build_response: dict = self.client.create_dashboard(**template_definition)

        template = _DashboardPayload(
            dashboard_id=build_response["DashboardId"],
            aws_account_id=self.payload.aws_account_id,
            name=template_definition["Name"],
        )

        return template

    def sync_published_version(self):
        """
        Queries the QuickSight API for the active published version number
        and dynamically updates the dashboard payload asset.
        """

        self.version = int(self.describe()["Dashboard"]["Version"]["VersionNumber"])


## Helper Functions ##

def _get_path(file_name: str) -> _Path:
    """
    Constructs an absolute Path pointer pointing to local configuration resource JSONs.

    Args:
        file_name (str): The core filename without the .json file extension.

    Returns:
        _Path: The absolute filesystem path string container pointing to the resource file.
    """
    root_path: _Path = _Path(__file__).parent.parent.parent
    file_path: _Path = root_path / f"resources/config/dashboard/{file_name}.json"
    return file_path


def _build_template_definition(project_name: str, user_name: str, team_name: str) -> dict:
    """
    Fetches the base skeleton configuration dictionary and dynamically structures
    the unique Dashboard identifiers based on target operational context.

    Args:
        project_name (str): Core target tracking workspace local string label.
        user_name (str): The alias handle of the targeted operational user identity.
        team_name (str): Name structure tracking group operational alignment.

    Returns:
        dict: The final runtime request body dict parsed for building out remote endpoints.
    """

    dashboard_def = _fetch(_get_path("template_dashboard"))
    # {team}-{project_name}-{user}
    dashboard_def["DashboardId"] = f"{team_name}-{project_name}-dev-{user_name}-dashboard"
    # {user}-{project_name}-dashboard
    dashboard_def["Name"] = f"{user_name}-{project_name}-dashboard"

    return dashboard_def
