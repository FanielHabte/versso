from pathlib import Path

from versso.git.local.service import LocalRepo
from versso.git.remote.template.payload import TemplatePayload
from versso.git.remote.template.service import RemoteTemplate

def build_local_repo_payload(project_path: Path, project_name: str) -> RemoteTemplate:
    """
    Factory function to construct a verified AnalysisPayload instance.

    Maps configuration variables directly into the target immutable container module.

    :param project_path:
    :return: A populated AnalysisPayload data structure instance.
    """
    return LocalRepo(
        context=TemplatePayload(),
        local_path=project_path
    )