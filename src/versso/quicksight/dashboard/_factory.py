from versso.quicksight.dashboard._payload import DashboardPayload
from versso.quicksight.setup._context import Context
from versso.quicksight.dashboard._service import Dashboard


def build_dashboard_payload(dashboard_id: str, aws_account_id: str, alias: str) -> DashboardPayload:
    return DashboardPayload(
        id=dashboard_id,
        aws_account_id=aws_account_id,
        name=alias
    )


def build_dashboard(dashboard_payload: DashboardPayload, context: Context, client) -> Dashboard:
    """
    Factory function to construct a verified AnalysisPayload instance.

    Maps configuration variables directly into the target immutable container module.

    :return: A populated AnalysisPayload data structure instance.
    """
    return Dashboard(
        dashboard_payload=dashboard_payload,
        context=context,
        quicksight_client=client
    )
