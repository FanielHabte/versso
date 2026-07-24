from versso.quicksight.folder._payload import FolderPayload as _FolderPayload
from versso.quicksight.folder._resource import Resource as _Resource


def build_folder_payload(aws_account_id: str, name: str, folder_id: str) -> _FolderPayload:
    """
    Factory function to construct a verified AnalysisPayload instance.

    Maps configuration variables directly into the target immutable container module.

    :param folder_id: The unique operational identifier for the target QuickSight analysis.
    :param aws_account_id: The numeric AWS Account ID hosting the infrastructure resources.
    :param name: The display or operational name assigned to the analysis object.
    :return: A populated AnalysisPayload data structure instance.
    """
    return _FolderPayload(
        id=folder_id,
        aws_account_id=aws_account_id,
        name=name
    )


def build_dev_folder_payload(aws_account_id: str, user_name: str) -> _FolderPayload:
    return _FolderPayload(
        id=f"{user_name}-dev-folder",
        aws_account_id=aws_account_id,
        name=f"{user_name}-dev-folder"
    )


def build_resource(resource: dict) -> _Resource:
    """
    Builds Resource payload from QuickSight API response.

    :param resource:
    :return: AnalysisRef| DatasetRef | DashboardRef
    """

    arn = resource["MemberArn"]
    r_type = arn.split(":")[-1].split("/")[0].upper()

    return _Resource(
        id=resource["MemberId"],
        arn=resource["MemberArn"],
        type=r_type
    )
