from versso.quicksight.folder._payload import FolderPayload as _FolderPayload, Resource


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


def build_reference_payload(resource: dict) -> Resource:
    """
    Builds Resource payload from QuickSight API response.

    :param resource:
    :return: AnalysisRef| DatasetRef | DashboardRef
    """

    arn = resource["MemberArn"]
    r_type = arn.split(":")[-1].split("/")[0].upper()

    return Resource(
        id=resource["MemberId"],
        arn=resource["MemberArn"],
        type=r_type
    )
