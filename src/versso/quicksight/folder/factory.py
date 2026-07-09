from versso.quicksight.folder.payload import FolderPayload


def build_folder_payload(aws_account_id: str, alias: str, folder_id: str) -> FolderPayload:
    """
    Factory function to construct a verified AnalysisPayload instance.

    Maps configuration variables directly into the target immutable container module.

    :param folder_id: The unique operational identifier for the target QuickSight analysis.
    :param aws_account_id: The numeric AWS Account ID hosting the infrastructure resources.
    :param alias: The display or operational name assigned to the analysis object.
    :return: A populated AnalysisPayload data structure instance.
    """
    return FolderPayload(
        folder_id=folder_id,
        aws_account_id=aws_account_id,
        name=alias
    )