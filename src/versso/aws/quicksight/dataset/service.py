from versso.aws.admin import client
import json

quick_client = client.build("us-east-1", "default")

def describe_dataset(account_id: str, dataset_id: str):
    analysis_description = quick_client.describe_dashboard(AwsAccountId=account_id, DataSetId=dataset_id)

    return json.loads(analysis_description)