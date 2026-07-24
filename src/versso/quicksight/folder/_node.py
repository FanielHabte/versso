from dataclasses import asdict
from dataclasses import dataclass

from versso.quicksight.folder._resource import Resource
import json


@dataclass(frozen=True)
class FolderNode:
    id: str
    name: str
    subfolders: list["FolderNode"]
    resources: list[Resource]

    def walk(self):
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

    def to_dict(self: "FolderNode"):
        return asdict(self)

    def to_json(self: "FolderNode"):
        json_str = json.dumps(asdict(self), indent=4)

        return json_str


def _find_resource(folder_node: FolderNode, requested_resources: list, resource_type: str):
    for resource in folder_node.resources:
        if resource_type == resource.type:
            requested_resources.append(resource)

    for subfolder in folder_node.subfolders:
        _find_resource(subfolder, requested_resources, resource_type)
