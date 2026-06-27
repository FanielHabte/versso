from versso.aws.admin import client
import json

quick_client = client.build("us-east-1", "default")

def describe_analysis(account_id: str, analysis_id: str):
    analysis_description = quick_client.describe_analysis(AwsAccountId=account_id, AnalysisId=analysis_id)

    return json.loads(analysis_description)