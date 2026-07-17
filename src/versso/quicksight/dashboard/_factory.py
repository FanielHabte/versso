from versso.quicksight.dashboard._payload import DashboardPayload


def build_dashboard_payload(dashboard_id: str, aws_account_id: str, alias: str) -> DashboardPayload:
    return DashboardPayload(
        dashboard_id=dashboard_id,
        aws_account_id=aws_account_id,
        name=alias
    )
