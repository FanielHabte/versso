import json
from pathlib import Path

from versso.quicksight.folder._payload import FolderPayload
from versso.quicksight.folder._resource import Resource
from versso.quicksight.folder._node import FolderNode
from versso.quicksight.setup._context import Context
from versso.util.helper import fetch


class Folder:

    def __init__(self, context: Context, client, payload: FolderPayload):
        self.context = context
        self.client = client
        self.payload = payload

    def add_resource(self, resource: Resource):
        service = resource.build_service(context=self.context, client=self.client)
        service_copy = service.clone()

        kwargs = {
            "AwsAccountId": service_copy.payload.aws_account_id,
            "FolderId": self.payload.id,
            "MemberId": service_copy.payload.id,
            "MemberType": resource.type
        }

        self.client.create_folder_membership(**kwargs)

    def add_resources(self, resources: list[Resource]):
        for resource in resources:
            self.add_resource(resource)

    def add_subfolder(self, folder_name: str):
        child_template = load_child_template(parent=self, child_folder_name=folder_name)

        child_payload = FolderPayload(
            id=child_template["FolderId"],
            aws_account_id=self.payload.aws_account_id,
            name=folder_name
        )

        child_folder = Folder(
            payload=child_payload,
            context=self.context,
            client=self.client
        )

        self.client.create_folder(**child_template)

        return child_folder

    def add_subfolders(self, node: FolderNode):
        for node in node.subfolders:
            sub_folder = self.add_subfolder(
                node.name
            )
            self.add_resources(node.resources)
            sub_folder.add_subfolders(node)

    def create(self) -> dict:
        create_response = self.client.create_folder(**self._load_template())
        j_string = json.dumps(create_response, indent=2)
        print("Successfully built Folder: \n", j_string)

        return create_response

    def clone_to(self, folder: "Folder"):
        # fetch tree
        nodes = self.tree()
        # if folder not exists create it
        folder.create()
        folder.add_subfolders(node=nodes)

    def define(self):
        description = self.client.describe_folder()
        description["Permissions"] = self.client.describe_folder_permissions()["Permissions"]

        return description

    def describe(self) -> dict:
        kwargs = {
            "AwsAccountId": self.payload.aws_account_id,
            "FolderId": self.payload.id
        }

        return self.client.describe_folder(**kwargs)

    def exists(self) -> bool:
        response = self.describe()

        return response["Status"] == 200

    def promote_to(self, target):
        pass

    def resources(self) -> list[Resource]:
        kwargs = {
            "AwsAccountId": self.payload.aws_account_id,
            "FolderId": self.payload.id
        }

        response = self.client.list_folder_members(**kwargs)

        return _build_resources(response["FolderMemberList"])

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
            raise RuntimeError(f"Folder {self.payload.name} (id: {self.payload.id}) doesn't exists")

        subfolders = _parse_sub_folders(
            subfolders=response["FolderSummaryList"],
            folder=self
        )

        return subfolders

    def tree(self) -> FolderNode:
        # initialize a dict with a parent id as key
        parent_node = _node_builder(self)

        # call recursive
        _build_nodes(self, parent_node)

        return parent_node

    def _load_template(self):
        template = _load_config("template")

        template["AwsAccountId"] = self.payload.aws_account_id
        template["Name"] = self.payload.name
        template["FolderId"] = self.payload.id
        template["Permissions"][0]["Principal"] = build_principal_arn(self)
        template["Tags"][0]["Value"] = self.context.project["name"]

        return template


def _parse_sub_folders(folder: Folder, subfolders: list[dict]) -> list["Folder"]:
    if len(subfolders) == 0:
        return list()

    subfolders_list = []
    for subfolder in subfolders:
        folder_payload = FolderPayload(
            id=subfolder["FolderId"],
            aws_account_id=folder.payload.aws_account_id,
            name=subfolder["Name"]
        )

        folder = Folder(
            context=folder.context,
            client=folder.client,
            payload=folder_payload
        )
        subfolders_list.append(folder)

    return subfolders_list


## Helper Functions ##

def _get_path(file_name: str):
    root_path = Path(__file__).parent.parent.parent
    file_path = root_path / f"resources/config/folder/{file_name}.json"

    return file_path


def _load_config(file_name: str):
    folder_config = fetch(_get_path(file_name))

    return folder_config


def _parse_folder_id(folder_arn: str) -> str:
    return folder_arn.rsplit("/")[-1]


def build_folder_id_arn(folder: Folder) -> str:
    region = folder.context.aws["region"]
    account_id = folder.payload.aws_account_id
    folder_id = folder.payload.id

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

    return _load_config("permission")[user_type]


## User Parent folder: username-dev-folder
## Project folder: username-dev-projectname
## Subfolder: username-dev-projectname-subfolder(datasets)

##


def build_folder_id(folder: Folder, cleaned_folder_name: str):
    user_name = folder.context.user["name"]
    project_name = folder.context.project["name"]

    return f"{user_name}-dev-{project_name}-{cleaned_folder_name}"


def load_child_template(parent: Folder, child_folder_name: str):
    template = _load_config("template")

    clean_folder_name = child_folder_name.lower().replace(' ', '_')
    template["AwsAccountId"] = parent.payload.aws_account_id
    template["Name"] = child_folder_name
    template["FolderId"] = build_folder_id(parent, clean_folder_name)
    template["ParentFolderArn"] = build_folder_id_arn(parent)
    template["Permissions"][0]["Principal"] = build_principal_arn(parent)
    template["Tags"][0]["Value"] = parent.context.project["name"]

    return template


def _build_resources(members_list: list[dict]) -> list[Resource]:
    resources: list[Resource] = []

    for resource in members_list:
        arn = resource["MemberArn"]
        r_type = arn.split(":")[-1].split("/")[0].upper()

        resource_payload = Resource(
            id=resource["MemberId"],
            arn=resource["MemberArn"],
            type=r_type
        )

        resources.append(resource_payload)

    return resources


def _node_builder(folder: Folder) -> FolderNode:
    return FolderNode(
        id=folder.payload.id,
        name=folder.payload.name,
        subfolders=[],
        resources=folder.resources()
    )


def _build_nodes(parent_folder: Folder, node: FolderNode) -> None:
    # check if the there are sub folder
    for child_folder in parent_folder.subfolders():
        child_node = _node_builder(folder=child_folder)
        node.subfolders.append(child_node)

        # call it's self
        _build_nodes(child_folder, child_node)
