from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardPayload:
    dashboard_id: str
    aws_account_id: str
    name: str
