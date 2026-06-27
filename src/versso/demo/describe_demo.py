import botocore.session as session
from botocore.stub import Stubber
import json
from pathlib import Path

qs = session.get_session().create_client("aws", "us-east-1")
root = Path(__file__).resolve().parent.parent.parent
dashboard_path = root / "resources/demo/dashboard.json"
analysis_path = root / "resources/demo/analysis.json"
dataset_one_path = root / "resources/demo/dataset_one.json"
dataset_two_path = root / "resources/demo/dataset_two.json"


def get_resource_def(resource_path):
    with open(resource_path, "r") as file:
        return json.load(file)


def describe_dashboard_definition(resource_path):
    expected_params = {
        "AwsAccountId": "123456789012",
        "DashboardId": "sales-performance-dashboard"
    }

    with Stubber(qs) as stubber:
        stubber.add_response("describe_dashboard_definition", get_resource_def(resource_path), expected_params)
        service_response = qs.describe_dashboard_definition(
            AwsAccountId="123456789012",
            DashboardId="sales-performance-dashboard"
        )

    return service_response

def describe_analysis_definition(resource_path):
    expected_params = {
        "AwsAccountId": "123456789012",
        "AnalysisId": "sales-performance-analysis"
    }

    with Stubber(qs) as stubber:
        stubber.add_response("describe_analysis_definition", get_resource_def(resource_path), expected_params)
        service_response = qs.describe_analysis_definition(
            AwsAccountId="123456789012",
            AnalysisId="sales-performance-analysis"
        )

    return service_response

def describe_dataset_two_definition(resource_path):
    expected_params = {
        "AwsAccountId": "123456789012",
        "DataSetId": "sales-orders-spice"
    }

    with Stubber(qs) as stubber:
        stubber.add_response("describe_data_set", get_resource_def(resource_path), expected_params)
        service_response = qs.describe_data_set(
            AwsAccountId="123456789012",
            DataSetId="sales-orders-spice"
        )

    return service_response

if __name__ == "__main__":
    print(describe_analysis_definition(analysis_path))
    print(describe_dashboard_definition(dashboard_path))
    print(describe_dataset_two_definition(dataset_two_path))