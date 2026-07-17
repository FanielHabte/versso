from versso import quicksight, git
from versso.quicksight import Folder

context = quicksight.Context.load()
builder = quicksight.Builder(context)

client = builder.build_client()
prod_folder = quicksight.Folder(
    context=context,
    payload=quicksight.FolderPayload(
        folder_id="central-analytics-team-admin-folder",
        aws_account_id="679432970382",
        name="Web-Analytics"
    ),
    client=client
)


resources = prod_folder.all_resources()

print(resources)
