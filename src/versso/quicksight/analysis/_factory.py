from versso.quicksight.setup._context import Context
from versso.quicksight.analysis._payload import AnalysisPayload
from versso.quicksight.analysis._service import Analysis


def build_analysis_payload(analysis_id: str, aws_account_id: str, name: str) -> AnalysisPayload:
    """
    Factory function to construct a verified AnalysisPayload instance.

    Maps configuration variables directly into the target immutable container module.

    :param analysis_id: The unique operational identifier for the target QuickSight analysis.
    :param aws_account_id: The numeric AWS Account ID hosting the infrastructure resources.
    :param name: The display or operational name assigned to the analysis object.
    :return: A populated AnalysisPayload data structure instance.
    """
    return AnalysisPayload(
        id=analysis_id,
        aws_account_id=aws_account_id,
        name=name
    )


def build_analysis(analysis_payload: AnalysisPayload, context: Context, client) -> Analysis:
    """
    Factory function to construct a verified AnalysisPayload instance.

    Maps configuration variables directly into the target immutable container module.

    :return: A populated AnalysisPayload data structure instance.
    """
    return Analysis(
        analysis_payload=analysis_payload,
        context=context,
        quicksight_client=client
    )
