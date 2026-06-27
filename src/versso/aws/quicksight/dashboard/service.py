from versso.aws.admin import client
import json

quick_client = client.build("us-east-1", "default")


def describe(account_id: str, dashboard_id: str):
    dashboard_description = quick_client.describe_dashboard(AwsAccountId=account_id, DashboardId=dashboard_id)

    return json.loads(dashboard_description)











