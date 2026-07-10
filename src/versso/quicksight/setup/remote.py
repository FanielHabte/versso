# Reads .verso/builder.json from the lead's prod repo
# (AWS account, dashboard ID, team-folder path). Deep-copies the prod dashboard folder
#  from the team folder into the BIE's own QS folder — a fresh analysis resource pointing at the prod dataset.json
#  (read-only). Cuts a local branch bie/<user>/<feature>.
from dataclasses import dataclass
from re import compile
import versso

# gt folder id
# recursively fetch the members of the folder to copy and paste them
# get folder members
#

@dataclass()
class BranchPayload:
    aws_account_id: str
    dashboard_id: str
    dashboard_folder_id: str
    user_parent_folder_id: str

    def __post_init__(self):
        account_id_pattern = compile(r"^[0-9]{12}$")
        dashboard_id_pattern = compile(r"[\w\-]+")

        if not dashboard_id_pattern.match(self.dashboard_id):
            raise ValueError("DashboardId didn't match the expected pattern")
        if not account_id_pattern.match(self.aws_account_id):
            raise ValueError("AwsAccountId didn't match the expected pattern")


def get_config_details():
    print("Please provide the below details to remote cloning")
    aws_account_id = input("Aws account id: ")
    dashboard_id = input("QuickSight id: ")
    dashboard_folder_id = input("Containing folder id: ")
    user_parent_folder_id = input("Your parent folder id: ")

    return aws_account_id, dashboard_id, dashboard_folder_id, user_parent_folder_id


def copy_resources(branch_payload: BranchPayload) -> None:
    existing_folder = versso.FolderPayload(
        id=branch_payload.dashboard_folder_id,
        aws_account_id=branch_payload.aws_account_id)

    user_folder = versso.FolderPayload(
        id=branch_payload.user_parent_folder_id,
        aws_account_id=branch_payload.aws_account_id)

    versso.folder_clone(existing_folder, user_folder)


def clone() -> bool:
    aws_account_id, dashboard_id, dashboard_folder_id, user_parent_folder_id = get_config_details()
    branch_payload = BranchPayload(aws_account_id, dashboard_id, dashboard_folder_id, user_parent_folder_id)
    copy_resources(branch_payload)

    return True