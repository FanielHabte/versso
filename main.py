from versso import quicksight

context = quicksight.Context.load()
builder = quicksight.Builder(context)

project_folder = builder.build_project_folder()
subfolder = project_folder.subfolders()

print(subfolder[0].add_subfolder("test"))
