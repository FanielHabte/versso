from typing import Any

from versso.util.helper import get_manifest_file
from versso.aws.quicksight.analysis.payload import AnalysisPayload


def build_prod_analysis_payload() -> AnalysisPayload:
    manifest: dict[str, Any] = get_manifest_file()
    analysis_id = manifest["analyses"]["prod"]["id"]
    analysis_alias = manifest["analyses"]["prod"]["alias"]
    aws_account_id = manifest["aws"]["id"]

    return AnalysisPayload(analysis_id=analysis_id,
                           aws_account_id=aws_account_id,
                           name=analysis_alias)