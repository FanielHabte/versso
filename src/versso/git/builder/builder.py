from pathlib import Path

from versso.git.local.payload import LocalRepoPayload
from versso.git.local.service import LocalRepo
from versso.quicksight import Context


def _build_path(directory: str):
    project_path = Path(directory)

    if not project_path.exists():
        raise RuntimeError(f"{project_path} is not a valid directory")
    return project_path


class Builder:
    def __init__(self, context: Context):
        self.context = context

    def build_local_repo_payload(self) -> LocalRepoPayload:
        project_context = self.context.project
        return LocalRepoPayload(
            path=_build_path(project_context["path"]),
            name=project_context["name"]
        )

    def build_local_repo(self) -> LocalRepo:
        """
        Factory function to construct a verified AnalysisPayload instance.

        Maps configuration variables directly into the target immutable container module.

        :return: A populated AnalysisPayload data structure instance.
        """
        return LocalRepo(
            context=self.context,
            local_repo_payload=self.build_local_repo_payload()
        )
