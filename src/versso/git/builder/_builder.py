from pathlib import Path

from versso.git.local._payload import LocalRepoPayload as _LocalRepoPayload
from versso.git.local._service import LocalRepo as _LocalRepo
from versso.quicksight import Context as _Context


def _build_path(directory: str):
    project_path = Path(directory)

    if not project_path.exists():
        raise RuntimeError(f"{project_path} is not a valid directory")
    return project_path


class Builder:
    def __init__(self, context: _Context):
        self.context = context

    def build_local_repo_payload(self) -> _LocalRepoPayload:
        project_context = self.context.project
        return _LocalRepoPayload(
            path=_build_path(project_context["path"]),
            name=project_context["name"]
        )

    def build_local_repo(self) -> _LocalRepo:
        """
        Factory function to construct a verified AnalysisPayload instance.

        Maps configuration variables directly into the target immutable container module.

        :return: A populated AnalysisPayload data structure instance.
        """
        return _LocalRepo(
            context=self.context,
            local_repo_payload=self.build_local_repo_payload()
        )
