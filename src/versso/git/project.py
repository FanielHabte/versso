from pathlib import Path
import re
import os
from versso.git import local

BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"


def get_name() -> str:
    """
    Collects project name from user.

    Return:
        str: project_name
    """
    while True:
        project_name: str = input("Please provide your project name: ").lower()
        pattern: str = r"^[a-z_]+$"

        if re.match(pattern, project_name):
            print(f"\n  {CYAN}●{RESET} Validating project name... Done ({project_name})")
            break
        print("\n** Please enter a valid name using only lowercase letters and underscores. **", end="\n")

    return project_name


def build_path(project_name: str) -> Path:
    """
    Builds project path from the current working directory.

    Args:
        project_name (str): project name that the user inputted
    Returns:
        Path: project_path (Path object)
    """
    root_path: Path = Path(os.getcwd()).resolve()
    project_path: Path = root_path / project_name

    return project_path


def build_local_repo(project_path: Path) -> bool:
    """
    Builds and initializes a local repo from a remote template.

    Args:
        project_path (Path): project path (equivalent to current working directory)
    Returns:
        bool: status of the process (True/False)
    """
    if not project_path.exists():
        local_repo.build(project_path)
        print(f"  {CYAN}●{RESET} Setting up repository structure... Done")
        return True
    else:
        raise Exception(
            f"Cannot clone template: Directory '{project_path}' already exists. Please delete it or choose a different path and try again.")


def rename_temp_names(parent_dir_name: str, project_path: Path, project_name: str) -> bool:
    """
    Renames temp names used in the directory of the template repo to project name

    Args:
        parent_dir_name (str): parent directory of the folders (src/test)
        project_name (str): project name replacing temp names
        project_path (Path): project path (equivalent to current working directory)
    Returns:
        bool: status of the process (True/False)
    """
    old_project_dir: Path = project_path / f"{parent_dir_name}/template"
    new_project_dir: Path = project_path / f"{parent_dir_name}/{project_name}"
    old_project_dir.replace(new_project_dir)

    return True


def initialize() -> None:
    """
    Orchestrates the creation and initialization of a new project.

    This function coordinates three modular functions to prompt the user,
    clone a remote template, and customize the directory structure.

    The orchestration follows these steps:
        1. Collects the project name from the user.
        2. Builds the project path using the current working directory.
        3. Clones and initializes a local repository from a remote template.
        4. Renames temporary placeholder names within the template directory
           to match the new project name.

    Returns:
        None
    """
    print("▲ VERSSO | Project Initialization \n")

    project_name: str = get_name()
    project_path: Path = build_path(project_name)

    if build_local_repo(project_path):
        rename_temp_names("src", project_path, project_name)
        rename_temp_names("test", project_path, project_name)
    print(f"  {CYAN}●{RESET} Configuring project source and tests... Done\n")

    print(f"{BOLD}{GREEN}✔ Success!{RESET} Project '{project_name}' built successfully.")


if __name__ == "__main__":
    initialize()
