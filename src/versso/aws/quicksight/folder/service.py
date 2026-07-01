from pathlib import Path

from versso.aws.quicksight.account.client import build
from versso.tools.helper import fetch


def setup_environment(quicksight_client, env_type: str):
    file_names = ["parent", "project", "analyses", "dashboard", "dataset"]

    for file_name in file_names:
        team_folder_config = get_folder_config(file_name, env_type)
        quicksight_client.create_folder(**team_folder_config)
        print(f"Created {file_name}!")

    return "Built all folders successfully!"


## Helper Functions ##

def get_folder_config(file_name: str, env_type: str):
    folder_config = fetch(get_path(file_name, env_type))

    return folder_config


def get_path(file_name: str, env_type: str):
    root_path = Path("/Users/fanielhabte/PycharmProjects/versso")
    file_path = root_path / f"src/versso/resources/config/folder/{env_type}/{file_name}.json"

    return file_path


if __name__ == "__main__":
    qs_client = build(profile_name="default", region="us-east-1")
    setup_environment(quicksight_client=qs_client, env_type="dev")
    setup_environment(quicksight_client=qs_client, env_type="prod")
