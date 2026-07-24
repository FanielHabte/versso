from versso.quicksight import Context
from versso.quicksight.analysis._payload import AnalysisPayload
from versso.quicksight.dashboard._payload import DashboardPayload
from versso.quicksight.dataset._payload import DatasetPayload

from versso.quicksight.dashboard._service import Dashboard
from versso.quicksight.analysis._service import Analysis
from versso.quicksight.dataset._service import Dataset

from dataclasses import dataclass


@dataclass(frozen=True)
class Resource:
    id: str
    arn: str
    type: str

    def build_payload(self, aws_account_id, client) -> AnalysisPayload | DashboardPayload | DatasetPayload:
        rs_type = self.type
        rs_id = self.id
        if rs_type == "ANALYSIS":
            return AnalysisPayload.build_payload(
                analysis_id=rs_id,
                aws_account_id=aws_account_id,
                client=client
            )
        elif rs_type == "DASHBOARD":
            return DashboardPayload.build_payload(
                dashboard_id=rs_id,
                aws_account_id=aws_account_id,
                client=client
            )
        elif rs_type == "DATASET":
            return DatasetPayload.build_payload(
                dataset_id=rs_id,
                aws_account_id=aws_account_id,
                client=client
            )
        else:
            raise RuntimeError(rs_type, 'is not a valid type')

    def build_service(self, context: Context, client) -> Dashboard | Dataset | Analysis:
        rs_type = self.type
        payload = self.build_payload(
            aws_account_id=context.aws["id"],
            client=client
        )

        if rs_type == "ANALYSIS":
            return Analysis(
                analysis_payload=payload,
                context=context,
                quicksight_client=client
            )
        elif rs_type == "DASHBOARD":
            return Dashboard(
                dashboard_payload=payload,
                context=context,
                quicksight_client=client
            )
        elif rs_type == "DATASET":
            return Dataset(
                dataset_payload=payload,
                context=context,
                quicksight_client=client
            )
        else:
            raise RuntimeError(rs_type, 'is not a valid type')


def _format_name(resource_name, user_name):
    return user_name + '-' + str(resource_name).lower().replace(' ', '-')
