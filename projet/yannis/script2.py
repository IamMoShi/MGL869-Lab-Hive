from utils import treeVersions
import git
import logging

def main():
    # Configuration du logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Cloner ou accéder au dépôt Git de Hive
    repo_path = "../hive"
    repo = git.Repo(repo_path)
    treeVersions(repo)
