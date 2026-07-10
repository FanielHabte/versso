from versso import quicksight, git

context = quicksight.Context.load()
git_builder = git.Builder(context=context)
local_repo = git_builder.build_local_repo()

local_repo.build()