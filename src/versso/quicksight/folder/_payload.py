import json
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class FolderPayload:
    folder_id: str
    aws_account_id: str
    name: str


@dataclass(frozen=True)
class Resource:
    id: str
    arn: str
    type: str


@dataclass(frozen=True)
class FolderNode:
    id: str
    name: str
    subfolders: list["FolderNode"]
    resources: list[Resource]

    @classmethod
    def walk(cls):
        pass

    def find(self, resource_type: str):
        if resource_type not in ("DASHBOARD", "ANALYSIS", "DATASET"):
            raise RuntimeError("Please provide valid type input [DASHBOARD, ANALYSIS, DATASET]")

        requested_resources: list[Resource] = []
        _find_resource(
            folder_node=self,
            requested_resources=requested_resources,
            resource_type=resource_type
        )

        return requested_resources

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        json_str = json.dumps(asdict(self), indent=4)

        return json_str


def _find_resource(folder_node: FolderNode, requested_resources: list, resource_type: str):
    for resource in folder_node.resources:
        if resource_type == resource.type:
            requested_resources.append(resource)

    for subfolder in folder_node.subfolders:
        _find_resource(subfolder, requested_resources, resource_type)