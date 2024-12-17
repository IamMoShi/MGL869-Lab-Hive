from datetime import datetime
import time
import sys
import subprocess
import git
import csv
import logging
import os
import re
from collections import defaultdict
from projet.yannis.tree import Node, print_tree, visualize_tree

class Metrics():
    def __init__(self, repo : git.Repo, currentVersion : str, previousVersion : str, file_path : str):
        self.version = currentVersion
        self.commitId = repo.git.rev_parse(currentVersion)
        self.file = file_path
        self.addedLines = self.addedLinesFunc(currentVersion, previousVersion, self.file)
        self.removedLines = self.removedLinesFunc(currentVersion, previousVersion, self.file)
        self.nbCommits = self.nbCommitsFunc(currentVersion, previousVersion, self.file)
        self.nbCommitsPreviousSolveBug = self.nbCommitsPreviousSolveBugFunc(currentVersion, self.file)
        self.nbCommitsPreviousEdited = self.nbCommitsPreviousEditedFunc(currentVersion, self.file)
        self.nbDevelopers = self.nbDevelopersFunc(currentVersion, previousVersion, self.file)
        self.nbDevelopersPrevious = self.nbDevelopersPreviousFunc(currentVersion, self.file)
        self.averageTimeBetweenEdits = self.averageTimeBetweenEditsFunc(currentVersion, previousVersion, self.file)
        self.averageTimeBetweenEditsPrevious = self.averageTimeBetweenEditsPreviousFunc(currentVersion, self.file)
        self.averageExpertiseDeveloper = self.averageExpertiseDeveloperFunc(currentVersion, previousVersion, self.file)
        self.minimumExpertiseDeveloper = self.minimumExpertiseDeveloperFunc(currentVersion, previousVersion, self.file)
        self.nbCommitsCommentEdited = self.nbCommitsCommentEditedFunc(currentVersion, previousVersion, self.file)
        self.nbCommitsNoCommentEdited = self.nbCommitsNoCommentEditedFunc(currentVersion, previousVersion, self.file)

        self.bugStatus = 0 #TODO
    
    def addedLinesFunc(self, currentVersion : str, previousVersion : str, file_path : str):
        '''
        Nombre de lignes ajoutées au fichier file_path dans la version currentVersion par rapport à la version previousVersion
        Dev Status : OK
        '''
        result = subprocess.run(
            ["git", "diff", f"{previousVersion}", currentVersion, "--", file_path],
            capture_output=True, text=True
        )
        diff_output = result.stdout
        added_lines = sum(1 for line in diff_output.splitlines() if line.startswith('+') and not line.startswith('+++'))
        return added_lines
    
    def removedLinesFunc(self, currentVersion : str, previousVersion : str, file_path : str):
        '''
        Nombre de lignes supprimées du fichier file_path dans la version currentVersion par rapport à la version previousVersion
        Dev Status : OK
        '''
        result = subprocess.run(
            ["git", "diff", f"{previousVersion}", currentVersion, "--", file_path],
            capture_output=True, text=True
        )
        diff_output = result.stdout
        removed_lines = sum(1 for line in diff_output.splitlines() if line.startswith('-') and not line.startswith('---'))
        return removed_lines
    
    def nbCommitsFunc(self, currentVersion : str, previousVersion : str, file_path : str):
        '''
        Nombre de commits qui ont modifié le fichier file_path entre les versions previousVersion et currentVersion
        Dev Status : OK
        '''
        result = subprocess.run(
            ["git", "log", "--oneline", f"{previousVersion}..{currentVersion}", "--", file_path],
            capture_output=True, text=True
        )
        return len(result.stdout.splitlines())

    def nbCommitsPreviousSolveBugFunc(self, currentVersion : str, file_path : str):
        '''
        Parmi les commits précédents à la version currentVersion, le nombre de commits qui ont corrigé un bug
        Dev Status : OK
        '''
        # Mots-clés pour identifier un commit corrigeant un bug
        bug_keywords = ["fix", "bug", "wrong", "invalid", "failed", "unable", "patch"] # Wrong result
        
        # Obtenir tous les commits précédents à la version actuelle pour le fichier
        result = subprocess.run(
            ["git", "log", "--pretty=format:%H %s", f"{currentVersion}~1", "--", file_path],
            capture_output=True, text=True
        )
        log_output = result.stdout
        
        # Filtrer les commits contenant des mots-clés
        bug_fix_commits = [
            line for line in log_output.splitlines()
            if any(keyword.lower() in line.lower() for keyword in bug_keywords)
        ]
        
        # Retourner le nombre de commits
        return len(bug_fix_commits)
    
    def nbCommitsPreviousEditedFunc(self, currentVersion : str, file_path : str):
        '''
        Parmi les commits précédents à la version currentVersion et currenVersion, le nombre de commits qui ont modifié le fichier file_path
        Dev Status : OK
        '''
        result = subprocess.run(
            ["git", "log", "--oneline", f"{currentVersion}", "--", file_path],
            capture_output=True, text=True
        )
        return len(result.stdout.splitlines())

    def nbDevelopersFunc(self, currentVersion : str, previousVersion : str, file_path : str):
        '''
        Nombre de développeurs qui ont modifié le fichier file_path dans la version currentVersion
        Dev Status : OK
        '''
        # Exécuter la commande git log pour obtenir les auteurs des commits
        result = subprocess.run(
            ["git", "log", "--format=%aN", f"{previousVersion}..{currentVersion}", "--", file_path],
            capture_output=True, text=True
        )

        # Séparer les résultats par ligne et éliminer les doublons
        authors = set(result.stdout.splitlines())
        
        # Retourner le nombre d'auteurs distincts
        return len(authors)

    def nbDevelopersPreviousFunc(self, currentVersion : str, file_path : str):
        '''
        Nombre de développeurs qui ont modifié le fichier file_path dans la version previousVersion
        Dev Status : OK
        '''
        # Exécuter la commande git log pour obtenir les auteurs des commits
        result = subprocess.run(
            ["git", "log", "--format=%aN", f"{currentVersion}", "--", file_path],
            capture_output=True, text=True
        )

        # Séparer les résultats par ligne et éliminer les doublons
        authors = set(result.stdout.splitlines())
        
        # Retourner le nombre d'auteurs distincts
        return len(authors)
    
    def averageTimeBetweenEditsFunc(self, currentVersion : str, previousVersion : str, file_path : str):
        '''
        Temps moyen entre les modifications du fichier file_path dans la version currentVersion
        Dev Status : OK
        '''
        # Exécuter la commande git log pour obtenir les dates des commits affectant le fichier
        result = subprocess.run(
            ["git", "log", "--format=%ad", "--date=iso", f"{previousVersion}..{currentVersion}", "--", file_path],
            capture_output=True, text=True
        )

        # Séparer les résultats par ligne pour obtenir les dates de chaque commit
        commit_dates = result.stdout.splitlines()

        # Si aucun commit n'a été trouvé, retourner None ou 0 pour indiquer qu'il n'y a pas de modifications
        if len(commit_dates) < 2:
            return None

        # Format de la date retournée par git (exemple : '2011-11-17 04:48:41 +0000')
        git_date_format = "%Y-%m-%d %H:%M:%S %z"

        # Convertir les dates de commit en objets datetime
        commit_times = [datetime.strptime(date, git_date_format) for date in commit_dates]

        # Calculer les différences de temps entre chaque commit successif
        time_diffs = []
        for i in range(1, len(commit_times)):
            time_diffs.append(abs((commit_times[i] - commit_times[i-1]).total_seconds()))

        # Calculer la moyenne des différences de temps
        average_time = sum(time_diffs) / len(time_diffs)

        # Retourner le temps moyen en secondes
        return average_time

    def averageTimeBetweenEditsPreviousFunc(self, currentVersion : str, file_path : str):
        '''
        Temps moyen entre les modifications du fichier file_path dans la version previousVersion
        Dev Status : OK
        '''
        # Exécuter la commande git log pour obtenir les dates des commits affectant le fichier
        result = subprocess.run(
            ["git", "log", "--format=%ad", "--date=iso", f"{currentVersion}", "--", file_path],
            capture_output=True, text=True
        )

        # Séparer les résultats par ligne pour obtenir les dates de chaque commit
        commit_dates = result.stdout.splitlines()

        # Si aucun commit n'a été trouvé, retourner None ou 0 pour indiquer qu'il n'y a pas de modifications
        if len(commit_dates) < 2:
            return None

        # Format de la date retournée par git (exemple : '2011-11-17 04:48:41 +0000')
        git_date_format = "%Y-%m-%d %H:%M:%S %z"

        # Convertir les dates de commit en objets datetime
        commit_times = [datetime.strptime(date, git_date_format) for date in commit_dates]

        # Calculer les différences de temps entre chaque commit successif
        time_diffs = []
        for i in range(1, len(commit_times)):
            time_diffs.append(abs((commit_times[i] - commit_times[i-1]).total_seconds()))

        # Calculer la moyenne des différences de temps
        average_time = sum(time_diffs) / len(time_diffs)

        # Retourner le temps moyen en secondes
        return average_time
    
    def averageExpertiseDeveloperFunc(self, currentVersion : str, previousVersion : str, file_path : str):
        '''
        Expertise moyenne des développeurs qui ont modifié le fichier file_path dans la version currentVersion
        Expertise d'un développeur signifie le nombre de commits que le développeur a effectués sur le fichier file_path
        Dev Status : OK
        '''
        
        # Exécuter la commande git log pour obtenir les commits entre previousVersion et currentVersion pour le fichier
        result = subprocess.run(
            ["git", "log", "--pretty=format:%H %an", f"{previousVersion}..{currentVersion}", "--", file_path],
            capture_output=True, text=True
        )
        
        # Récupérer les commits avec leur auteur
        commits = result.stdout.splitlines()
        
        # Créer un dictionnaire pour compter le nombre de commits par auteur
        developer_commits = defaultdict(int)
        
        for commit in commits:
            commit_hash, author = commit.split(' ', 1)
            # Incrémenter le compteur de commits pour cet auteur
            developer_commits[author] += 1
        
        # Calculer la moyenne de l'expertise (moyenne du nombre de commits par auteur)
        if developer_commits:
            average_expertise = sum(developer_commits.values()) / len(developer_commits)
        else:
            average_expertise = 0
        
        # Retourner la moyenne de l'expertise des développeurs
        return average_expertise
    
    def minimumExpertiseDeveloperFunc(self, currentVersion : str, previousVersion : str, file_path : str):
        '''
        Expertise minimale des développeurs qui ont modifié le fichier file_path dans la version currentVersion
        Expertise d'un développeur signifie le nombre de commits que le développeur a effectués sur le fichier file_path
        Dev Status : OK
        '''
        # Exécuter la commande git log pour obtenir les commits entre previousVersion et currentVersion pour le fichier
        result = subprocess.run(
            ["git", "log", "--pretty=format:%H %an", f"{previousVersion}..{currentVersion}", "--", file_path],
            capture_output=True, text=True
        )
        
        # Récupérer les commits avec leur auteur
        commits = result.stdout.splitlines()
        
        # Créer un dictionnaire pour compter le nombre de commits par auteur
        developer_commits = defaultdict(int)
        
        for commit in commits:
            commit_hash, author = commit.split(' ', 1)
            # Incrémenter le compteur de commits pour cet auteur
            developer_commits[author] += 1
        
        # Calculer l'expertise minimale
        if developer_commits:
            min_expertise = min(developer_commits.values())
        else:
            min_expertise = 0
        
        # Retourner l'expertise minimale
        return min_expertise
    
    def nbCommitsCommentEditedFunc(self, currentVersion : str, previousVersion : str, file_path : str):
        '''
        Nombre de commits qui ont modifié un commentaire du fichier file_path dans la version currentVersion
        Dev Status : 
        '''
        # Exécuter la commande git log pour obtenir les commits entre previousVersion et currentVersion pour le fichier
        result = subprocess.run(
            ["git", "log", "--pretty=format:%H", f"{previousVersion}..{currentVersion}", "--", file_path],
            capture_output=True, text=True
        )
        
        # Récupérer les hashes des commits
        commits = result.stdout.splitlines()
        
        # Initialiser le compteur pour les commits ayant modifié des commentaires
        comment_edits_count = 0
        
        # Définir un ensemble de symboles de commentaires pour Java
        comment_symbols = ['//', '/*', '*/']
        
        # Pour chaque commit, vérifier s'il modifie un commentaire
        for commit in commits:
            # Obtenir les différences du commit (diff) pour ce fichier spécifique
            diff_result = subprocess.run(
                ["git", "diff", f"{commit}^!", "--", file_path],
                capture_output=True, text=True, encoding="utf-8"
            )
            
            # Vérifier les changements dans le diff
            diff_output = diff_result.stdout
            
            if not diff_output:
                continue

            # Parcourir les lignes du diff pour trouver les lignes modifiées qui sont des commentaires
            for line in diff_output.splitlines():
                # Vérifier si la ligne modifiée est un commentaire (commence par un symbole de commentaire)
                if any(line.strip().startswith(symbol) for symbol in comment_symbols):
                    if line.startswith('+') or line.startswith('-'):
                        logging.info(f"Line: {line}")
                        comment_edits_count += 1
                    break  # Si un commentaire est trouvé dans ce commit, on passe au suivant
        
        # Retourner le nombre de commits qui ont modifié un commentaire
        return comment_edits_count
    
    def nbCommitsNoCommentEditedFunc(self, currentVersion : str, previousVersion : str, file_path : str):
        '''
        Nombre de commits qui ont modifié le code du fichier file_path sans modifier de commentaire dans la version currentVersion
        Dev Status : 
        '''
        # Exécuter la commande git log pour obtenir les commits entre previousVersion et currentVersion pour le fichier
        result = subprocess.run(
            ["git", "log", "--pretty=format:%H", f"{previousVersion}..{currentVersion}", "--", file_path],
            capture_output=True, text=True
        )
        
        # Récupérer les hashes des commits
        commits = result.stdout.splitlines()
        
        # Initialiser le compteur pour les commits qui ont modifié du code sans toucher aux commentaires
        no_comment_edits_count = 0
        
        # Définir un ensemble de symboles de commentaires pour Java
        comment_symbols = ['//', '/*', '*/']
        
        # Pour chaque commit, vérifier s'il modifie uniquement du code sans toucher aux commentaires
        for commit in commits:
            # Obtenir les différences du commit (diff) pour ce fichier spécifique
            diff_result = subprocess.run(
                ["git", "diff", f"{commit}^!", "--", file_path],
                capture_output=True, text=True, encoding="utf-8"
            )
            
            # Vérifier les changements dans le diff
            diff_output = diff_result.stdout

            if not diff_output:
                continue
            
            # Flag pour vérifier si le commit modifie du code sans toucher aux commentaires
            modified_code = False
            
            # Parcourir les lignes du diff pour trouver les lignes modifiées qui sont du code (et pas un commentaire)
            for line in diff_output.splitlines():
                # Si la ligne modifiée commence par un symbole de commentaire, ignorer
                if any(line.strip().startswith(symbol) for symbol in comment_symbols):
                    continue
                
                # Si la ligne modifiée n'est pas un commentaire, c'est du code modifié
                if line.startswith('+') or line.startswith('-'):
                    modified_code = True
                    break
            
            # Si du code a été modifié sans modifier de commentaire, incrémenter le compteur
            if modified_code:
                no_comment_edits_count += 1
        
        # Retourner le nombre de commits ayant modifié du code sans modifier de commentaire
        return no_comment_edits_count

    @staticmethod
    def collectMetrics(file_path, repo, version, previousVersion) -> dict:
        metrics = Metrics(repo, version, previousVersion, file_path)
        return metrics.__dict__

def logProcess(idx,total_files,start_time):
    # Calcul du pourcentage de progression
    percent_complete = (idx / total_files) * 100
    
    # Temps écoulé et estimation du temps restant
    elapsed_time = time.time() - start_time
    avg_time_per_file = elapsed_time / idx
    estimated_total_time = avg_time_per_file * total_files
    time_remaining = estimated_total_time - elapsed_time

    # Log de progression
    sys.stdout.write(
        f"\rProcessed {idx}/{total_files} files ({percent_complete:.2f}%). "
        f"Elapsed: {elapsed_time:.2f}s, Remaining: {time_remaining:.2f}s."
    )
    sys.stdout.flush()

def exportCsv(metrics: list, output_file: str):
    logging.info("Exporting in CSV...")

    if not metrics:
        logging.warning("No data to export")
        return
    
    # Ouvrir le fichier en mode écriture
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        # Créer un écrivain CSV
        fieldnames = metrics[0].keys()  # Utilise les clés du premier dictionnaire comme en-têtes
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Écrire les en-têtes
        writer.writeheader()
        
        # Écrire les lignes de données
        writer.writerows(metrics)

    logging.info("CSV exported successfully")

def treeVersions(repo, show=False) -> Node:
    '''
    Retourne un arbre des versions du dépôt Git
    '''
    logging.info("Building version tree...")
    # Obtenir toutes les versions du dépôt
    tags = repo.tags
    versions = [tag.name for tag in tags]

    logging.info(f"Found {len(versions)} versions")
    
    # Créer un dictionnaire pour stocker les relations entre les versions
    version_tree = {}
    
    # Parcourir les versions pour construire l'arbre
    for version in versions:
        version_numbers = re.compile(r'\d+\.\d+').search(version)
        if version_numbers:
            version_numbers = tuple([int(k) for k in version_numbers.group().split('.')])
        else:
            continue
        currentDir = os.getcwd()
        work_tree = f"{currentDir}\\data\\temp_repositories\\hive"
        git_dir = f"{work_tree}\\.git"
        dateReleaseCmd = subprocess.run(
            ["git", f"--git-dir={git_dir}", "log", "-1", f"--format=%ai", version],
            capture_output=True,
            text=True
        )
        dateReleaseStr = dateReleaseCmd.stdout.strip()
        date_format = "%Y-%m-%d %H:%M:%S %z" # 2021-05-01 12:00:00 +0200
        dateRelease = datetime.strptime(dateReleaseStr, date_format)

        version_tree[version] = {
            "numbers": version_numbers,
            "date": dateRelease,
        }

    versionTree = sorted(version_tree.items(), key=lambda x: x[1]["date"])
    filteredVTree = [s for s in versionTree if re.match(r'.*\.0$', s[0])] # patch versions
    filteredVTree = [s for s in filteredVTree if not re.match(r'.*rc\d$', s[0])] # rc0, rc1, rc2, ...
    filteredVTree = [s for s in filteredVTree if not re.match(r'.*storage.*', s[0])] # storage-release
    filteredVTree = [s for s in filteredVTree if not re.match(r'.*alpha.*', s[0])] # alpha-1, alpha-2, ...
    filteredVTree = [s for s in filteredVTree if not re.match(r'.*beta.*', s[0])] # beta-1, beta-2, ...
    filteredVTree = [s for s in filteredVTree if not re.match(r'.*standalone.*', s[0])] # standalone-metastore

    Vtree = [Node(s) for s in filteredVTree][::-1]
    logging.info(f"Filtered version tree size: {len(filteredVTree)}")
    for ptrV1 in range(len(Vtree)-1):
        childNode = Vtree[ptrV1]
        candidateParentNode = Vtree[ptrV1+1]
        ptrV2 = 0
        while candidateParentNode.value[1]["numbers"] > childNode.value[1]["numbers"]:
            ptrV2 += 1
            if ptrV1+1+ptrV2 >= len(filteredVTree):
                break
            candidateParentNode = Vtree[ptrV1+1+ptrV2]
        candidateParentNode.add_child(childNode)
        childNode.parent = candidateParentNode
        
    if show:
        print_tree(candidateParentNode)
        visualize_tree(candidateParentNode).view()
    logging.info("Version tree built successfully")
    return candidateParentNode

def previousVersionFunc(version : str, treeVersion : Node) -> str:
    '''
    Retourne la version précédente à la version donnée dans l'arbre des versions
    Status : OK
    '''
    # Si la version recherchée est la valeur du nœud actuel, aucun parent à retourner
    if treeVersion.value[0] == version:
        return None
    
    # Sinon, explorez tous les enfants du nœud
    if treeVersion.children:
        for child in treeVersion.children:
            # Si la version recherchée est un enfant direct
            if child.value[0] == version:
                return treeVersion.value[0]
            # Si la version recherchée est dans les descendants de cet enfant
            else:
                parent = previousVersionFunc(version, child)
                if parent:  # Si on trouve un parent dans la sous-arborescence
                    return parent

    # Si le nœud n'est pas trouvé dans l'arbre
    return None