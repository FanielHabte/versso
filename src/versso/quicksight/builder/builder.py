__all__ = ["Builder"]

from versso.quicksight.account._factory import build_client as _build_client

from versso.quicksight.analysis.factory import build_analysis_payload as _build_analysis_payload
from versso.quicksight.analysis.payload import AnalysisPayload as _AnalysisPayload
from versso.quicksight.analysis.service import Analysis as _Analysis

from versso.quicksight.dashboard.factory import build_dashboard_payload as _build_dashboard_payload
from versso.quicksight.dashboard.payload import DashboardPayload as _DashboardPayload
from versso.quicksight.dashboard.service import Dashboard as _Dashboard

from versso.quicksight.setup.context import Context

from versso.quicksight.folder.service import Folder as _Folder
from versso.quicksight.folder.payload import FolderPayload as _FolderPayload
from versso.quicksight.folder.factory import build_folder_payload as _build_folder_payload


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

        return _build_analysis_payload(
            analysis_id=_prod_config["id"],
            aws_account_id=self.aws_account_id,
            alias=_prod_config["alias"]
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

        return _build_dashboard_payload(
            dashboard_id=_prod_config["id"],
            aws_account_id=self.aws_account_id,
            alias=_prod_config["alias"]
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
        project_config = self.context.folder["project"]

        return _build_folder_payload(
            folder_id=project_config["id"],
            alias=project_config["name"],
            aws_account_id=self.aws_account_id
        )

    def build_project_folder(self) -> _Folder:
        return _Folder(
            payload=self.build_project_folder_payload(),
            client=self.build_client(),
            context=self.context
        )
