from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetPayload:
    id: str
    aws_account_id: str
    name: str

    @classmethod
    def build_payload(cls, dataset_id: str, aws_account_id: str, client):
        kwargs = {
            "AwsAccountId": aws_account_id,
            "DatasetId": dataset_id
        }
        response = client.describe_dashboard(**kwargs)

        return DatasetPayload(
            id=dataset_id,
            aws_account_id=aws_account_id,
            name=response["Name"]
        )
