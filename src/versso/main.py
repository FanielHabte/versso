# from git import Repo
# import pathlib
#
# path_dir = pathlib.Path("test_dir")
#
# if not path_dir.exists():
#     repo_url = "https://github.com/gitpython-developers/QuickStartTutorialFiles.git"
#     repo = Repo.clone_from(repo_url, path_dir)


def say_hi(name:str):
    """
        Function that takes name input and prints Hi + name as an output

        Args:
            name (str): the name of the user

        Returns:
             None
    """
    print(f"Hi {name}")
