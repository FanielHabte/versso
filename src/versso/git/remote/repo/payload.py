from dataclasses import dataclass


@dataclass
class RemoteRepoPayload:
    name: str = "versso_remote_template"
    git_address: str = "https://github.com/FanielHabte/vesso-template.git"
