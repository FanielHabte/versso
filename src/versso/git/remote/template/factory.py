from pathlib import Path

from versso.git.remote.template.payload import TemplatePayload
from versso.git.remote.template.service import RemoteTemplate

def build_remote_template(project_path: Path) -> RemoteTemplate:
    """
    Factory function to construct a verified AnalysisPayload instance.

    Maps configuration variables directly into the target immutable container module.

    :param project_path:
    :return: A populated AnalysisPayload data structure instance.
    """
    return RemoteTemplate(
        template_payload=TemplatePayload(),
        local_path=project_path
    )