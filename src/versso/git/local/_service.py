from pathlib import Path
from shutil import rmtree
from git import Repo

from versso.git.local._payload import LocalRepoPayload
from versso.git.remote.template.factory import build_remote_template
from versso.quicksight.setup._context import Context


class LocalRepo:

    def __init__(self, context: Context, local_repo_payload: LocalRepoPayload):
        self.context = context
        self.local_repo_payload = local_repo_payload
        self.remote_template = build_remote_template(project_path=self.local_repo_payload.path)

    def build(self):
        self.remote_template.clone()
        self.delete_git_file()
        rename_dirs(
            folder_names=["src", "test"],
            project_path=self.local_repo_payload.path,
            project_name=self.local_repo_payload.name
        )
        self.git_init()

    def git_init(self):
        Repo.init(self.local_repo_payload.path)

    def delete_git_file(self):
        dot_git = self.local_repo_payload.path / ".git"

        try:
            if dot_git.exists():
                rmtree(dot_git)
            else:
                raise FileNotFoundError(f"Error: {dot_git} not found")
        except OSError as e:
            raise OSError(f"Error: unable to delete .local_repo folder using rmtree.") from e


def rename_dirs(folder_names: list, project_path: Path, project_name: str) -> bool:
    """
    Renames temp names used in the directory of the remote repo to local name

    Args:
        folder_names (list): parent directory of the folders (src/test)
        project_name (str): local name replacing temp names
        project_path (Path): local path (equivalent to current working directory)
    Returns:
        bool: status of the process (True/False)
    """
    project_name = project_name.replace("-", "_")
    for folder_name in folder_names:
        old_project_dir: Path = project_path / f"{folder_name}/template"
        new_project_dir: Path = project_path / f"{folder_name}/{project_name}"
        old_project_dir.replace(new_project_dir)

    return True
