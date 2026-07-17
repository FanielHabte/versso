from versso import quicksight, git

context = quicksight.Context.load()
builder = quicksight.Builder(context)

client = builder.build_client()
project_folder = builder.build_project_folder()

