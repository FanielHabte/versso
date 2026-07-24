__all__ = ["Builder"]

from versso.quicksight.account._factory import build_client as _build_client

from versso.quicksight.analysis._payload import AnalysisPayload as _AnalysisPayload
from versso.quicksight.analysis._service import Analysis as _Analysis

from versso.quicksight.dashboard._payload import DashboardPayload as _DashboardPayload
from versso.quicksight.dashboard._service import Dashboard as _Dashboard

from versso.quicksight.folder._service import Folder as _Folder
from versso.quicksight.folder._payload import FolderPayload as _FolderPayload
from versso.quicksight.setup._context import Context


class Builder:

    def __init__(self, context: Context):
        self.context = context
        self.aws_account_id = context.aws["id"]

    def build_prod_analysis_payload(self) -> _AnalysisPayload:
        """
        Constructs a production-targeted AnalysisPayload object using configurations
        extracted from the global system manifest.

        :return: A populated AnalysisPayload tailored for the production AWS account environment.
        """
        _prod_config: dict = self.context.analysis["prod"]

        return _AnalysisPayload(
            id=_prod_config["id"],
            aws_account_id=self.aws_account_id,
            name=_prod_config["alias"]
        )

    def build_client(self):
        """
        Initializes and provides the underlying boto3 QuickSight client wrapped
        with target AWS profile credentials and region definitions.
    
        :return: An authorized boto3 QuickSight service client instance.
        """
        _aws_config: dict = self.context.aws

        return _build_client(
            profile_name=_aws_config["profile"],
            region=_aws_config["region"]
        )

    def build_prod_dashboard_payload(self) -> _DashboardPayload:
        """
        Constructs a production-targeted DashboardPayload object using configurations
        extracted from the global system manifest.

        :return: A populated DashboardPayload tailored for the production AWS account environment.
        """
        _prod_config: dict = self.context.dashboard["prod"]

        return _DashboardPayload(
            id=_prod_config["id"],
            aws_account_id=self.aws_account_id,
            name=_prod_config["alias"]
        )

    def build_prod_dashboard(self) -> _Dashboard:
        """
        Factory function that instantiates and returns a fully initialized production
        Dashboard service instance linked to the active QuickSight client.

        Returns:
            Dashboard: An operational Dashboard service manager targeting the production environment.
        """
        return _Dashboard(
            context=self.context,
            dashboard_payload=self.build_prod_dashboard_payload(),
            quicksight_client=self.build_client()
        )

    def build_prod_analysis(self) -> _Analysis:
        """
        Factory function that instantiates and returns a fully initialized production
        Analysis service instance linked to the active QuickSight client.

        Returns:
            Analysis: An operational Analysis service manager targeting the production environment.
        """
        return _Analysis(
            analysis_payload=self.build_prod_analysis_payload(),
            context=self.context,
            quicksight_client=self.build_client()
        )

    def build_project_folder_payload(self) -> _FolderPayload:
        project_config = self.context.folder["parent"]

        return _FolderPayload(
            id=project_config["id"],
            name=project_config["name"],
            aws_account_id=self.aws_account_id
        )

    def build_project_folder(self) -> _Folder:
        return _Folder(
            payload=self.build_project_folder_payload(),
            client=self.build_client(),
            context=self.context
        )

    def build_my_dev_folder_payload(self) -> _FolderPayload:
        user_name = self.context.user["name"]
        return _FolderPayload(
            id=f"{user_name}-dev-folder",
            aws_account_id=self.aws_account_id,
            name=f"{user_name}-dev-folder"
        )

    def build_my_dev_folder(self) -> _Folder:
        return _Folder(
            context=self.context,
            client=self.build_client(),
            payload=self.build_my_dev_folder_payload()
        )
