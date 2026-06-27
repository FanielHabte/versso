from versso.aws.admin import client
from multipledispatch import dispatch
import json

quick_client = client.build("us-east-1", "default")


@dispatch(str, str)
def pull(account_id: str, analysis_id: str) -> str:
    """
    Pulls latest description of the given **Analysis** from QuickSight api.

    :param account_id:
    :param analysis_id:
    :return: analysis_description
    """
    analysis_description = quick_client.describe_analysis(AwsAccountId=account_id, AnalysisId=analysis_id)

    return json.loads(analysis_description)


@dispatch(str, str, int)
def pull(account_id: str, analysis_id: str, version: int) -> str:
    """
    Pulls the specific version of the analysis description from QuickSight api.

    :param account_id:
    :param analysis_id:
    :param version:
    :return: analysis_description (JSON)
    """
    analysis_description = quick_client.describe_analysis(AwsAccountId=account_id, AnalysisId=analysis_id,
                                                          Version=version)

    return json.loads(analysis_description)


def update():
    pass
