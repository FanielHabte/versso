from dataclasses import dataclass


@dataclass(frozen=True)
class AnalysisRef:
    id: str
    arn: str


@dataclass(frozen=True)
class DashboardRef:
    id: str
    arn: str


@dataclass(frozen=True)
class DatasetRef:
    id: str
    arn: str


@dataclass(frozen=True)
class FolderNode:
    id: str
    name: str
    subfolders: list["FolderNode"]
    resources: list[AnalysisRef | DashboardRef | DatasetRef]

    @classmethod
    def walk(cls):
        pass
