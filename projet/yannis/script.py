import git
from datetime import datetime
import logging
import time
import sys
from utils import logProcess, exportCsv, treeVersions, previousVersionFunc
from utils import Metrics

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Cloner ou accéder au dépôt Git de Hive
repo_path = "../hive"
repo = git.Repo(repo_path)
tree = treeVersions(repo)

# Version à analyser
version = "rel/release-2.3.0"
logging.info(f"Switching to version: {version}")
repo.git.checkout(version)
previousVersion = previousVersionFunc(version, tree)
logging.info(f"Previous version: {previousVersion}")

# Obtenir la liste des fichiers dans le dépôt
files = repo.git.ls_files().splitlines()

# Prendre les 100 premiers fichiers
files_sorted = sorted(files)
files = files_sorted[:100]

logging.info(f"Total number of files to analyze: {len(files)}")
total_files = len(files)

# Collecter les métriques pour chaque fichier
start_time = time.time()
metrics = []

logging.info("Starting metrics collection...")
for idx, file_path in enumerate(files, start=1):
    
    file_metrics = Metrics.collectMetrics(file_path, repo, version, previousVersion)
    metrics.append(file_metrics)
    logProcess(idx,total_files,start_time)

sys.stdout.write("\n")
logging.info("Metrics collection finished")

# Afficher les métriques collectées
# for m in metrics[:15]:
    # print(m)

exportCsv(metrics, "../MGL869-Final-Project/metrics.csv")