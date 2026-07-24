from versso import quicksight, git

context = quicksight.Context.load()
builder = quicksight.Builder(context)
client = builder.build_client()

# project_folder = builder.build_project_folder()
# my_dev_folder = builder.build_my_dev_folder()
#
# project_folder.clone_to(folder=my_dev_folder)

print(client.describe_data_set(
    AwsAccountId='679432970382',
    DataSetId='a6a7c2fb-ea0a-484a-9d76-a002c0f683b0'
))