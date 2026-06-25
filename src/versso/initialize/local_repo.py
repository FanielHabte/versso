from git import Repo
from pathlib import Path
from shutil import rmtree


def clone_template(project_path: Path):
    Repo.clone_from("https://github.com/FanielHabte/vesso-template.git", project_path)


def delete_git_folder(project_path: Path):
    dot_git = project_path / ".git"

    try:
        if dot_git.exists():
            rmtree(dot_git)
        else:
            raise FileNotFoundError(f"Error: {project_path} not found")
    except OSError as e:
        raise OSError(f"Error: unable to delete .git folder using rmtree.") from e


def initiate(project_path: Path):
    Repo.init(project_path)


def build(project_path:Path) -> bool:

    clone_template(project_path)
    delete_git_folder(project_path)
    initiate(project_path)

    return True