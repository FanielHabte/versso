from typing import Any

from versso.aws.account.payload import AwsAccountPayload


def build_aws_payload(aws_config: dict[str, Any]):
    return AwsAccountPayload(id=aws_config["id"],
                             region=aws_config["region"],
                             alias=aws_config["alias"])
