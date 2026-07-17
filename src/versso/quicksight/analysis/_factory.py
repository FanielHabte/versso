from versso.quicksight.analysis._payload import AnalysisPayload


def build_analysis_payload(analysis_id: str, aws_account_id: str, alias: str) -> AnalysisPayload:
    """
    Factory function to construct a verified AnalysisPayload instance.

    Maps configuration variables directly into the target immutable container module.

    :param analysis_id: The unique operational identifier for the target QuickSight analysis.
    :param aws_account_id: The numeric AWS Account ID hosting the infrastructure resources.
    :param alias: The display or operational name assigned to the analysis object.
    :return: A populated AnalysisPayload data structure instance.
    """
    return AnalysisPayload(
        analysis_id=analysis_id,
        aws_account_id=aws_account_id,
        name=alias
    )