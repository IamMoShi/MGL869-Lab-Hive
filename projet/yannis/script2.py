from utils import treeVersions
import git
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

repo_path = "../hive"
repo = git.Repo(repo_path)
treeVersions(repo)