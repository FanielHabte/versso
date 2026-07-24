from versso.quicksight.dataset._payload import DatasetPayload as _DatasetPayload
from versso.quicksight.interfaces._i_service import Service
from time import sleep as _sleep
from versso.util.helper import fetch as _fetch
from pathlib import Path as _Path


class Dataset(Service):

    def __init__(self, dataset_payload, context, quicksight_client):
        super().__init__(payload=dataset_payload, context=context, client=quicksight_client)

    def create(self):
        pass

    def define(self) -> dict:
        """
        Pulls the latest configuration details of the given Dataset from the QuickSight API.

        Note: AWS QuickSight does not have a `describe_data_set_definition` API like Analysis,
        so `describe_data_set` is used to retrieve structural definitions (e.g., PhysicalTableMap, LogicalTableMap).

        :return: A dictionary containing the full configuration dictionary of the datasets.
        """

        kwargs: dict = {
            "AwsAccountId": self.payload.aws_account_id,
            "DataSetId": self.payload.dataset_id
        }
        return self.client.describe_data_set(**kwargs)["DataSet"]

    def describe(self) -> dict:
        """
        Retrieves the top-level description and metadata status of the Dataset.

        :return: A dictionary representing the AWS API response for describe_data_set.
        """
        kwargs: dict = {
            "AwsAccountId": self.payload.aws_account_id,
            "DataSetId": self.payload.dataset_id
        }
        return self.client.describe_data_set(**kwargs)

    def update(self, definition: dict) -> dict:
        """
        Updates the given Dataset with the provided definition mapping and blocks
        until the QuickSight deployment or ingestion completes.

        :param definition: The target schema/mapping dictionary for the datasets.
        :raises RuntimeError: If the update process fails on the AWS server side.
        :return: The initial update response dictionary from the client.
        """

        kwargs: dict = {
            "AwsAccountId": self.payload.aws_account_id,
            "DataSetId": self.payload.dataset_id,
            "Name": self.payload.name,
            "PhysicalTableMap": definition.get("PhysicalTableMap"),
            "LogicalTableMap": definition.get("LogicalTableMap"),
            "ImportMode": definition.get("ImportMode", "DIRECT_QUERY")
        }

        update_response: dict = self.client.update_data_set(**kwargs)

        while True:
            # Poll status check from API response or describe output
            status_code: int = update_response.get("Status")

            if status_code == 200:
                return update_response

            if status_code >= 400:
                raise RuntimeError(f"Failed to update datasets {self.payload.dataset_id}")

            _sleep(5)

    def clone(self) -> "Dataset":
        """
        Creates a duplicate instance of the current datasets using a remote-built workspace.

        :return: A new, updated Dataset object mimicking this instance's schema.
        """

        response = self._create_template()

        template_payload = _DatasetPayload(
            id=response["DataSetId"],
            aws_account_id=self.payload.aws_account_id,
            name=response["Name"],
        )

        copy: "Dataset" = Dataset(
            dataset_payload=template_payload,
            context=self.context,
            quicksight_client=self.client
        )

        copy.update(self.define())

        return copy

    def promote_to(self, target: "Dataset") -> "Dataset":
        """
        Push this datasets's definition into target (e.g. beta → prod).

        :param target: The target Dataset destination module.
        :return: The target Dataset object after updating.
        """
        target.update(self.define())
        return target

    def _create_template(self) -> dict:
        """
        Generates an initial datasets deployment shell derived from structural manifest details.

        :return: A response dictionary pointing to the newly generated remote placeholder datasets.
        """
        template_definition: dict = _build_template_definition(
            project_name=self.context.project["name"],
            user_name=self.context.user["alias"],
            dataset_name=self.payload.name,
        )

        return self.client.create_data_set(**template_definition)


def _get_path(file_name: str) -> _Path:
    """
    Resolves the absolute filepath to localized datasets configuration assets.

    :param file_name: The target file's prefix string.
    :return: A Path object mapped directly to the local system layout target JSON.
    """
    root_path: _Path = _Path(__file__).parent.parent.parent
    file_path: _Path = root_path / f"resources/config/datasets/{file_name}.json"
    return file_path


def _build_template_definition(project_name: str, user_name: str, dataset_name: str) -> dict:
    """
    Pulls base configurations and format names appropriately using standard deployment convention templates.

    Format schema utilizes:
    - ID: `{user_name}-{project_name}-datasets`
    - Display Name: `{user_name}-{dataset_name}`

    :param project_name: The explicit structural identification name for this codebase segment.
    :param user_name: The developer/runner alias.
    :param dataset_name: The target name string for the datasets.
    :return: A dictionary configured with unique identifiers ready for deployment payload operations.
    """
    dataset_def = _fetch(_get_path("template_dataset"))

    dataset_def["DataSetId"] = f"{user_name}-{project_name}-{dataset_name}-datasets"
    dataset_def["Name"] = f"{user_name}-{dataset_name}"

    return dataset_def
