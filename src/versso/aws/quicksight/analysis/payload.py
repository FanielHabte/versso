from dataclasses import dataclass
from re import compile


@dataclass()
class AnalysisPayload:
    id: str
    aws_account_id: str
    version: int = 0
    version_set: bool = False

    def __post_init__(self):
        account_id_pattern = compile(r"^[0-9]{12}$")
        analysis_id_pattern = compile(r"[\w\-]+")

        if not analysis_id_pattern.match(self.id):
            raise ValueError("AnalysisId didn't match the expected pattern")
        if not account_id_pattern.match(self.aws_account_id):
            raise ValueError("AwsAccountId didn't match the expected pattern")
