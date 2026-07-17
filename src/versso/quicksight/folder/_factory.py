from versso.quicksight.folder._payload import FolderPayload as _FolderPayload
from versso.quicksight.folder._resources import DatasetRef, DashboardRef, AnalysisRef


def build_folder_payload(aws_account_id: str, alias: str, folder_id: str) -> _FolderPayload:
    """
    Factory function to construct a verified AnalysisPayload instance.

    Maps configuration variables directly into the target immutable container module.

    :param folder_id: The unique operational identifier for the target QuickSight analysis.
    :param aws_account_id: The numeric AWS Account ID hosting the infrastructure resources.
    :param alias: The display or operational name assigned to the analysis object.
    :return: A populated AnalysisPayload data structure instance.
    """
    return _FolderPayload(
        folder_id=folder_id,
        aws_account_id=aws_account_id,
        name=alias
    )


def build_reference_payload(resource: dict) -> DatasetRef | DashboardRef | AnalysisRef:
    """
    Builds resources reference payloads based on the type.

    :param resource:
    :return: AnalysisRef| DatasetRef | DashboardRef

    :raises: RuntimeError
    """

    arn = resource["MemberArn"]
    r_type = arn.split(":")[-1].split("/")[0].upper()

    if r_type == "DATASET":
        return DatasetRef(
            id=resource["MemberId"],
            arn=resource["MemberArn"]
        )
    elif r_type == "DASHBOARD":
        return DashboardRef(
            id=resource["MemberId"],
            arn=resource["MemberArn"]
        )
    elif r_type == "ANALYSIS":
        return AnalysisRef(
            id=resource["MemberId"],
            arn=resource["MemberArn"]
        )

    raise RuntimeError(
        f"Type {r_type} is not a valid type or not supported at this time. Here are the supported type [Dataset, Analysis, Dashboard]")
