import json

from versso import quicksight, git

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

j_string = json.dumps(prod_folder.all_resources(), indent=2)

print(j_string)
