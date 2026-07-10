from shutil import rmtree
from git import Repo

from versso.git.local.payload import LocalRepoPayload
from versso.git.remote.template.factory import build_remote_template
from versso.quicksight.setup.context import Context


class LocalRepo:

    def __init__(self, context: Context, local_repo_payload: LocalRepoPayload):
        self.context = context
        self.local_repo_payload = local_repo_payload
        self.remote_template = build_remote_template(project_path=self.local_repo_payload.path)

    def build(self):
        self.remote_template.clone()
        self.clean()
        self.init()

    def init(self):
        Repo.init(self.local_repo_payload.path)

    def clean(self):
        dot_git = self.local_repo_payload.path / ".git"

        try:
            if dot_git.exists():
                rmtree(dot_git)
            else:
                raise FileNotFoundError(f"Error: {dot_git} not found")
        except OSError as e:
            raise OSError(f"Error: unable to delete .local_repo folder using rmtree.") from e
