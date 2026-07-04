from versso.aws.account.factory import build_aws_payload
from versso.util.helper import get_manifest_file


def get_aws_account_payload():
    aws_config = get_manifest_file()["aws"]

    return build_aws_payload(aws_config=aws_config)