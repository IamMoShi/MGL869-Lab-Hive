import subprocess
from datetime import datetime

# La commande git
git_command = [
    "git", "log",
    "--numstat", "-p",
    "--pretty=format:%n%n%n***%nCommit: %H%nAuthor: %an <%ae>%nDate: %ad %nSubject: %s%n%n%n",
    "--ignore-all-space", "--cc", "--unified=0",
    "--encoding=UTF-8"
]

# Exécution de la commande avec subprocess
process = subprocess.Popen(
    git_command,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,  # Permet de lire directement en chaînes de caractères
    encoding="utf-8"
)

commits = []
diff = 0

try:
    commit = {}
    # Lire ligne par ligne
    for line in iter(process.stdout.readline, ""):  # iter garantit que readline boucle jusqu'à la fin
        line = line.strip()
        if diff:
            pass
        elif line:  # Ignore les lignes vides
            if line.startswith("Commit:"):
                if 'hash' in commit:
                    commits.append(commit)
                    print(commit['hash'])
                    commit = {}
                commit["hash"] = line.split(" ")[1]
            elif line.startswith("Author:"):
                commit["author"] = line.split(" ")[1] + "," + line.split(" ")[2]
            elif line.startswith("Date:"):
                # ex : Date: Mon Oct 28 20:17:16 2024 +0900
                commit["date"] = datetime.strptime(line[6:], "%a %b %d %H:%M:%S %Y %z")
            elif line.startswith("Subject:"):
                commit["subject"] = line[9:]
            elif line.startswith("diff"):
                file = {"filename": line.split(" ")[-1][2::]}
                commit["file"] = file
                print(file["filename"])
                break

        else:
            diff = 0

    # Attendre que le processus se termine complètement
    process.wait()

    # Vérifier si des erreurs sont survenues
    if process.returncode != 0:
        error_message = process.stderr.read()
        print(f"Error occurred: {error_message}")

except Exception as e:
    print(f"An exception occurred: {e}")

finally:
    process.stdout.close()
    process.stderr.close()
