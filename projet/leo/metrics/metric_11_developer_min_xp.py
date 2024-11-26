from Objects.Version import Version
from projet.leo.metrics.metric_10_developer_mean_xp import developer_count_version


def metric_11_developer_min_xp(file: str, version: Version):
    previous_version = version.getPreviousVersion()
    commits = version.getDiff()[file]['commits']
    developer_xp = developer_count_version(previous_version)
    min_xp = float('inf')

    for commit in commits:
        developer = commit.getAuthor()
        if developer in developer_xp:
            min_xp = min(min_xp, developer_xp[developer])

    if min_xp == float('inf'):
        return 0
    return min_xp
