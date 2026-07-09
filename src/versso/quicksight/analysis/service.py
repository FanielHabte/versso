__all__ = ["Analysis"]

from pathlib import Path as _Path
from versso.quicksight.analysis.payload import AnalysisPayload as _AnalysisPayload
from versso.quicksight.interfaces.i_service import Service
from versso.util.helper import fetch as _fetch
from time import sleep as _sleep
from versso.quicksight.setup.context import Context as _Context


class Analysis(Service):
    """
    Encapsulates Amazon QuickSight Analysis operations.

    Provides a clean interface to define, describe, update, clone, and promote
    QuickSight analyses utilizing an underlying QuickSight client and structural payloads.
    """

    def __init__(self, analysis_payload: _AnalysisPayload, context: _Context, quicksight_client):
        """
        Initializes the Analysis instance.

        :param analysis_payload: The configuration metadata for the target analysis.
        :param quicksight_client: An initialized boto3 QuickSight client.
        """
        super().__init__(payload=analysis_payload, context=context, client=quicksight_client)


    def create(self):
        pass

    def define(self) -> dict:
        """
        Pulls the latest definition of the given Analysis from the QuickSight API.

        :return: A dictionary containing the full visual/structural definition of the analysis.
        """
        kwargs: dict = {
            "AwsAccountId": self.payload.aws_account_id,
            "AnalysisId": self.payload.analysis_id
        }
        return self.client.describe_analysis_definition(**kwargs)["Definition"]

    def describe(self) -> dict:
        """
        Retrieves the top-level description and metadata status of the Analysis.

        :return: A dictionary representing the AWS API response for describe_analysis.
        """
        kwargs: dict = {
            "AwsAccountId": self.client.aws_account_id,
            "AnalysisId": self.client.analysis_id
        }
        return self.client.describe_analysis(**kwargs)

    def update(self, definition: dict) -> dict:
        """
        Updates the given Analysis with the provided definition and blocks
        until the QuickSight deployment job completes successfully.

        :param definition: The target layout and structural dictionary for the analysis.
        :raises RuntimeError: If the update process fails on the AWS server side.
        :return: The initial update response dictionary from the client.
        """
        kwargs: dict = {
            "AwsAccountId": self.payload.aws_account_id,
            "AnalysisId": self.payload.analysis_id,
            "Name": self.payload.name,
            "Definition": definition
        }

        update_response: dict = self.client.update_analysis(**kwargs)

        while True:
            status = self.describe()["Analysis"]["Status"]

            if status in ["CREATION_SUCCESSFUL", "UPDATE_SUCCESSFUL"]:
                return update_response

            if update_response["UpdateStatus"] == "UPDATE_FAILED":
                error_message = update_response["Error"]["Message"]
                raise RuntimeError(f"Failed to update analysis due to {error_message}")

            _sleep(5)

    def clone(self) -> "Analysis":
        """
        Creates a duplicate instance of the current analysis using a template-built workspace.

        :return: A new, updated Analysis object mimicking this instance's layout.
        """
        template_analysis: _AnalysisPayload = self._create_template()

        copy: "Analysis" = Analysis(
            analysis_payload=template_analysis,
            context=self.context,
            quicksight_client=self.client
        )

        copy.update(self.define())
        return copy

    def promote_to(self, target: "Analysis") -> "Analysis":
        """
        Push this analysis's definition into target (e.g. beta → prod).

        :param target: The target Analysis destination module.
        :return: The AWS update API response dictionary.
        """
        target.update(self.define())

        return target

    def _create_template(self) -> _AnalysisPayload:
        """
        Generates an initial analysis deployment shell derived from structural manifest details.

        :return: An active AnalysisPayload pointing to the newly generated template placeholder.
        """

        template_definition: dict = _build_template_definition(
            project_name=self.context.project["name"],
            user_name=self.context.user["alias"],
            team_name=self.context.team["name"]
        )

        build_response: dict = self.client.create_analysis(**template_definition)

        template = _AnalysisPayload(
            analysis_id=build_response["AnalysisId"],
            aws_account_id=self.payload.aws_account_id,
            name=template_definition["Name"],
        )

        return template


def _get_path(file_name: str) -> _Path:
    """
    Resolves the absolute filepath to localized configuration assets.

    :param file_name: The target file's prefix string.
    :return: A Path object mapped directly to the local system layout target JSON.
    """
    root_path: _Path = _Path(__file__).parent.parent.parent
    file_path: _Path = root_path / f"resources/config/analyses/{file_name}.json"
    return file_path


def _build_template_definition(project_name: str, user_name: str, team_name: str) -> dict:
    """
    Pulls base configurations and format names appropriately using standard deployment convention templates.

    Format schema utilizes:
    - ID: `{team}-{project_name}-{user}`
    - Display Name: `{user}-{project_name}-analysis`

    :param project_name: The explicit structural identification name for this codebase segment.
    :param user_name: The developer/runner alias.
    :param team_name: The organizational corporate division grouping tag.
    :return: A dictionary configured with unique identifiers ready for deployment payload operations.
    """
    analyses_def = _fetch(_get_path("template_analyses"))

    analyses_def["AnalysisId"] = f"{team_name}-{project_name}-{user_name}"
    analyses_def["Name"] = f"{user_name}-{project_name}-analysis"

    return analyses_def
