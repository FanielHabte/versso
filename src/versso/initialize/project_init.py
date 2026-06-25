from git import Repo
from pathlib import Path
import re
import os

BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"

def get_project_name():
    # Ask user for the project name
    while True:
        project_name = input("Please provide your project name: ").lower()
        pattern = r"^[a-z_]+$"

        if re.match(pattern, project_name):
            print(f"\n  {CYAN}●{RESET} Validating project name... Done ({project_name})")
            break
        print("\n** Please enter a valid name using only lowercase letters and underscores. **", end="\n")

    return project_name


def get_project_path(project_name: str) -> Path:
    root_path = Path(os.getcwd()).resolve()
    project_path = root_path / project_name

    return project_path


def clone_project_template(project_path: Path) -> bool:
    if not project_path.exists():
        Repo.clone_from("https://github.com/FanielHabte/vesso-template.git", project_path)
        print(f"  {CYAN}●{RESET} Setting up repository structure... Done")
        return True
    else:
        raise Exception(
            f"Cannot clone template: Directory '{project_path}' already exists. Please delete it or choose a different path and try again.")


def rename_placeholder_names(dir_type: str, project_path: Path, project_name: str) -> bool:
    old_project_dir = project_path / f"{dir_type}/template"
    new_project_dir = project_path / f"{dir_type}/{project_name}"
    old_project_dir.replace(new_project_dir)

    return True


def initialize_project():
    print("▲ VERSSO | Project Initialization \n")

    project_name = get_project_name()
    project_path = get_project_path(project_name)

    if clone_project_template(project_path):
        rename_placeholder_names("src", project_path, project_name)
        rename_placeholder_names("test", project_path, project_name)
    print(f"  {CYAN}●{RESET} Configuring project source and tests... Done\n")

    print(f"{BOLD}{GREEN}✔ Success!{RESET} Project '{project_name}' built successfully.")


if __name__ == "__main__":
    initialize_project()
