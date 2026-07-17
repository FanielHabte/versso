from pathlib import Path
from typing import Any

from versso.quicksight.folder._factory import build_folder_payload
from versso.quicksight.folder._payload import FolderPayload
from versso.quicksight.setup._context import Context
from versso.util.helper import fetch


class Folder:

    def __init__(self, context: Context, client, payload: FolderPayload):
        self.context = context
        self.client = client
        self.payload = payload

    def create(self) -> dict:
        return self.client.create_folder(**self._load_template())

    def add_subfolder(self, folder_name: str):
        child_template = load_child_template(parent=self, child_folder_name=folder_name)

        child_payload = build_folder_payload(
            aws_account_id=self.payload.aws_account_id,
            alias=folder_name,
            folder_id=child_template["FolderId"]
        )

        child_folder = Folder(
            payload=child_payload,
            context=self.context,
            client=self.client
        )

        self.client.create_folder(**child_template)

        return child_folder

    def exists(self) -> bool:
        response = self.describe()

        return response["Status"] == 200

    def define(self):
        description = self.client.describe_folder()
        description["Permissions"] = self.client.describe_folder_permissions()["Permissions"]

        return description

    def describe(self) -> dict:
        kwargs = {
            "AwsAccountId": self.payload.aws_account_id,
            "FolderId": self.payload.folder_id
        }

        return self.client.describe_folder(**kwargs)

    def clone(self):
        pass

    def promote_to(self, target):
        pass

    def subfolders(self) -> list["Folder"]:
        kwargs = {
            "AwsAccountId": self.payload.aws_account_id,
            "Filters": [
                {
                    "Operator": "StringEquals",
                    "Name": "PARENT_FOLDER_ARN",
                    "Value": build_folder_id_arn(self)
                }
            ]
        }

        response = self.client.search_folders(**kwargs)

        if not response["Status"] == 200:
            raise RuntimeError(f"Folder {self.payload.name} (id: {self.payload.folder_id}) doesn't exists")

        subfolders = _parse_sub_folders(
            subfolders=response["FolderSummaryList"],
            folder=self
        )

        return subfolders

    def resources(self) -> list[dict]:
        kwargs = {
            "AwsAccountId": self.payload.aws_account_id,
            "FolderId": self.payload.folder_id
        }

        response = self.client.list_folder_members(**kwargs)

        return _parse_resources(response["FolderMemberList"])

    def all_resources(self) -> dict[str, list]:
        # initialize a dict with a parent id as key
        all_resources: dict[str, Any] = {
            "id": self.payload.folder_id,
            "name": self.payload.name,
            "subfolders": [],
            "resources": self.resources()
        }

        # call recursive
        _recursive_folders(self, all_resources)

        return all_resources

    def _load_template(self):
        template = load_config("remote")

        template["AwsAccountId"] = self.payload.aws_account_id
        template["Name"] = self.payload.name
        template["FolderId"] = build_folder_id(self)
        template["Permissions"][0]["Principal"] = build_principal_arn(self)
        template["Tags"][0]["Value"] = self.context.project["name"]

        return template


def _parse_sub_folders(folder: Folder, subfolders: list[dict]) -> list["Folder"]:
    if len(subfolders) == 0:
        return list()

    subfolders_list = []
    for subfolder in subfolders:
        folder_payload = build_folder_payload(
            aws_account_id=folder.payload.aws_account_id,
            alias=subfolder["Name"],
            folder_id=subfolder["FolderId"]
        )

        folder = Folder(
            context=folder.context,
            client=folder.client,
            payload=folder_payload
        )
        subfolders_list.append(folder)

    return subfolders_list


## Helper Functions ##

def get_path(file_name: str):
    root_path = Path(__file__).parent.parent.parent
    file_path = root_path / f"resources/config/folder/{file_name}.json"

    return file_path


def load_config(file_name: str):
    folder_config = fetch(get_path(file_name))

    return folder_config


def _parse_folder_id(folder_arn: str) -> str:
    return folder_arn.rsplit("/")[-1]


def build_folder_id_arn(folder: Folder) -> str:
    region = folder.context.aws["region"]
    account_id = folder.payload.aws_account_id
    folder_id = folder.payload.folder_id

    return f"arn:aws:quicksight:{region}:{account_id}:folder/{folder_id}"


def build_principal_arn(folder: Folder) -> str:
    region = folder.context.aws["region"]
    account_id = folder.payload.aws_account_id
    user_alias = folder.context.user["id"]

    return f"arn:aws:quicksight:{region}:{account_id}:user/default/{user_alias}"


def get_permission(user_type: str) -> list[str]:
    valid_user_type = ["ADMIN", "VIEWER", "BUILDER"]
    if user_type not in valid_user_type:
        raise RuntimeError(f"{user_type} is not part of the valid choices {valid_user_type}")

    return load_config("permission")[user_type]


def build_folder_id(folder: Folder):
    team_name = folder.context.team["name"]
    user_alias = folder.context.user["alias"]
    project_name = folder.context.project["name"]

    return f"{team_name}-{user_alias}-{project_name}"


def load_child_template(parent: Folder, child_folder_name: str):
    template = load_config("remote")

    clean_folder_name = child_folder_name.lower().replace(' ', '_')
    template["AwsAccountId"] = parent.payload.aws_account_id
    template["Name"] = child_folder_name
    template["FolderId"] = build_folder_id(parent) + f"-{clean_folder_name}"
    template["ParentFolderArn"] = build_folder_id_arn(parent)
    template["Permissions"][0]["Principal"] = build_principal_arn(parent)
    template["Tags"][0]["Value"] = parent.context.project["name"]

    return template


def _parse_resources(resources_list: list[dict]):
    # "id": "172af51b-19c6-4802-bc95-b845de7ebad0",
    # "name": "Web Traffic Dataset",
    # "type": "DATASET",
    # "arn": "arn:aws:quicksight:us-east-1:679432970382:dataset/172af51b-19c6-4802-bc95-b845de7ebad0"

    for index, resource in enumerate(resources_list):
        arn = resource["MemberArn"]
        r_type = arn.split(":")[-1].split("/")[0].upper()

        parsed_strct = {
            "id": resource["MemberId"],
            "arn": resource["MemberArn"],
            "type": r_type,
        }

        resources_list[index] = parsed_strct

    return resources_list


def _recursive_folders(parent: Folder, all_resources: dict[str, Any]) -> None:
    # check if the there are sub folder
    for child in parent.subfolders():
        child_all_resources = {
            "id": child.payload.folder_id,
            "name": child.payload.name,
            "subfolders": [],
            "resources": child.resources()
        }

        all_resources["subfolders"].append(child_all_resources)

        # call it's self
        _recursive_folders(child, child_all_resources)
