from typing import Any

from versso.quicksight.folder._payload import FolderPayload


def find_resources_in_folder(folder_payload: Any, quick_client: Any) -> dict[str, list[str]]:
    """
    Orchestrates the retrieval of all QuickSight resources sitting inside the immediate
    subfolders of a given parent folder.

    Parameters:
        folder_payload (FolderPayload): Object containing the parent folder ID and AWS account ID.
        quick_client (Any): An initialized Boto3 QuickSight client instance.

    Returns:
        dict[str, list[str]]: A dictionary grouping gathered resource IDs by their type.
    """
    aws_account_id = folder_payload.aws_account_id
    parent_folder_id = folder_payload.id

    sub_folders = search_sub_folder(quick_client, aws_account_id, parent_folder_id)
    combined_resources: dict[str, list[str]] = {}

    for folder in sub_folders:
        folder_id: str = folder["FolderId"]
        folder_members = find_folder_members(quick_client, aws_account_id, folder_id)
        sub_folder_assets = get_resources(folder_members)

        for res_type, res_ids in sub_folder_assets.items():
            combined_resources.setdefault(res_type, []).extend(res_ids)

    print("Successfully saved")
    return combined_resources


### Helper Functions ###

def search_sub_folder(quick_client: Any, aws_account_id: str, parent_folder_id: str) -> list[dict[str, Any]]:
    """
    Queries the AWS account to find all folders that have the specified folder designated as their parent.

    Parameters:
        quick_client (Any): An initialized Boto3 QuickSight client instance.
        aws_account_id (str): The 12-digit AWS account ID.
        parent_folder_id (str): The unique ID string of the parent folder.

    Returns:
        list[dict[str, Any]]: A list of metadata summaries for each discovered subfolder.
    """
    sf_response = quick_client.search_folders(
        AwsAccountId=aws_account_id,
        Filters=[
            {
                'Name': 'PARENT_FOLDER_ARN',
                'Operator': 'StringEquals',
                'Value': f'arn:aws:quicksight:us-east-1:{aws_account_id}:folder/{parent_folder_id}'
            }
        ]
    )
    return sf_response.get('FolderSummaryList', [])


def find_folder_members(quick_client: Any, aws_account_id: str, folder_id: str) -> list[dict[str, Any]]:
    """
    Retrieves the raw list of immediate members (assets) contained directly within a specific folder.

    Parameters:
        quick_client (Any): An initialized Boto3 QuickSight client instance.
        aws_account_id (str): The 12-digit AWS account ID.
        folder_id (str): The unique ID string of the targeted folder.

    Returns:
        list[dict[str, Any]]: A raw list of member objects from the QuickSight API response payload.
    """
    lfm_response = quick_client.list_folder_members(
        AwsAccountId=aws_account_id,
        FolderId=folder_id
    )
    return lfm_response.get("FolderMemberList", [])


def get_resources(folder_members: list[dict[str, Any]]) -> dict[str, list[str]]:
    """
    Parses a raw list of folder members, extracts their resource type from the ARN,
    and groups their IDs into lists.

    Parameters:
        folder_members (list[dict[str, Any]]): A list of member objects containing MemberArn and MemberId.

    Returns:
        dict[str, list[str]]: A mapped dictionary categorizing resource IDs by type string.
    """
    members: dict[str, list[str]] = {}
    for resource in folder_members:
        # Extract resource type cleanly (e.g., 'dashboard', 'dataset.json')
        resource_type = str(resource["MemberArn"]).rsplit(":", 1)[-1].split("/")[0]
        members.setdefault(resource_type, []).append(resource["MemberId"])

    return members


if __name__ == "__main__":
    from versso.quicksight.account._service import get_qs_client_from_session

    qs_client = get_qs_client_from_session(region="us-east-1", profile_name="default")
    folder_obj = FolderPayload(folder_id="ee5dcacf-a64d-4dcd-bf14-cd11369eea27", aws_account_id="679432970382")
    response = find_resources_in_folder(folder_payload=folder_obj, quick_client=qs_client)

    print(response)
