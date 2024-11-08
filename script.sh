#!/bin/bash

export PATH=$PATH:/Applications/Understand.app/Contents/MacOS/

HIVE_DIR="../hive"
MGL_DIR="../MGL869-Lab-Hive"
LOG_DIR="$MGL_DIR/logs"
OUTPUT_FILE="$MGL_DIR/final_metrics.csv"
FILTERED_OUTPUT_FILE="$MGL_DIR/filtered_final_metrics.csv" 

mkdir -p "$LOG_DIR"
# Nom du fichier de log basé sur la date et l'heure
LOG_FILE="$LOG_DIR/log_$(date '+%Y-%m-%d_%H-%M-%S').log"

# Ajouter les en-têtes au fichier de sortie avec tous les noms de métriques
echo "Version,CommitId,Name,AvgCountLine,AvgCountLineBlank,AvgCountLineCode,AvgCountLineComment,AvgCyclomatic,CountClassBase,CountClassCoupled,CountClassCoupledModified,CountClassDerived,CountDeclClass,CountDeclClassMethod,CountDeclClassVariable,CountDeclExecutableUnit,CountDeclFile,CountDeclFunction,CountDeclInstanceMethod,CountDeclInstanceVariable,CountDeclMethod,CountDeclMethodAll,CountDeclMethodDefault,CountDeclMethodPrivate,CountDeclMethodProtected,CountDeclMethodPublic,CountInput,CountLine,CountLineBlank,CountLineCode,CountLineCodeDecl,CountLineCodeExe,CountLineComment,CountOutput,CountSemicolon,CountStmt,CountStmtDecl,CountStmtExe,Cyclomatic,MaxCyclomatic,MaxInheritanceTree,MaxNesting,PercentLackOfCohesion,PercentLackOfCohesionModified,RatioCommentToCode,SumCyclomatic,CountDeclFileCode,CountDeclFileHeader,CountDeclInstanceVariablePrivate,CountDeclInstanceVariableProtected,CountDeclInstanceVariablePublic,CountDeclMethodConst,CountDeclMethodFriend,CountLineInactive,CountLinePreprocessor,CountStmtEmpty,CountCCViol,CountCCViolType,CCViolDensityLine,CCViolDensityCode" > "$OUTPUT_FILE"

files_to_include=()
while IFS=, read -r issue_key file_path; do
    if [ "$issue_key" != "Issue Key" ]; then
        filename=$(basename "$file_path")
        files_to_include+=("$filename")
    fi
done < "$MGL_DIR/filtered_couples.csv"

# Charger les versions, dates et commits depuis commits_for_main_hive_versions.csv
while IFS=, read -r version release_date last_commit; do
    # Ignorer la première ligne (en-têtes)
    if [ "$version" == "version" ]; then
        continue
    fi

    # Supprimer les espaces ou caractères invisibles de fin de ligne dans le commit
    last_commit=$(echo "$last_commit" | tr -d '\r')

    echo "Processing version $version with release date $release_date and commit $last_commit"
    cd "$HIVE_DIR" || exit

    # Vérifier si le commit est présent
    if [ -z "$last_commit" ]; then
        echo "No commit found for version $version with release date $release_date"
        continue
    fi

    # echo "Analyzing version $version (commit $last_commit)"

    # git stash --include-untracked
    # git checkout "$last_commit" || exit

    # und purge "$MGL_DIR/analysis.und" 
    # und add "$HIVE_DIR" -db "$MGL_DIR/analysis.und" | tee -a "$LOG_FILE"
    # und analyze -db "$MGL_DIR/analysis.und" | tee -a "$LOG_FILE"

    # und metrics "$MGL_DIR/analysis.und"
    # mv "$MGL_DIR/analysis.csv" "$MGL_DIR/full_metrics_${version}.csv"

    # echo "Metrics for version $version saved to full_metrics_${version}.csv"
    
    # Filtrer les lignes où Kind est "File" et ajouter Version et CommitId au début de chaque ligne 
    awk -F, -v version="$version" -v commit="$last_commit" 'BEGIN {OFS = ","} 
    NR==1 {header=$0; next} 
    $1 == "File" {print version, commit, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31, $32, $33, $34, $35, $36, $37, $38, $39, $40, $41, $42, $43, $44, $45, $46, $47, $48, $49, $50, $51, $52, $53, $54, $55, $56, $57, $58, $59, $60, $61, $62}' "$MGL_DIR/full_metrics_${version}.csv" >> "$OUTPUT_FILE"

    echo "Filtered metrics for version $version saved to $OUTPUT_FILE"


    # Revenir à la branche principale (master)
    git checkout master
    
    break

done < "$MGL_DIR/commits_for_main_hive_versions.csv"

# # Créer une expression régulière pour `grep` afin de chercher les noms de fichiers dans final_metrics.csv
# pattern=$(printf "|%s" "${files_to_include[@]}")
# pattern="${pattern:1}"  # Supprime le premier '|'

# # Filtrer final_metrics.csv pour ne garder que les fichiers présents dans filtered_couples.csv
# awk -F, -v pattern="$pattern" 'NR==1 || $3 ~ pattern' "$OUTPUT_FILE" >> "$FILTERED_OUTPUT_FILE"

echo "Finished analyzing all versions"
