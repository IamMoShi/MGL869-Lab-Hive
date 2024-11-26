from Objects.Version import Version


def developer_count_version(version: Version):
    developer_xp: dict = dict()
    for commit in version.getCommitsLogs():
        developer = commit.getAuthor()
        if developer not in developer_xp:
            developer_xp[developer] = 0
        developer_xp[developer] += 1
    return developer_xp


def metric_10_developer_mean_xp(file: str, version: Version):
    previous_version = version.getPreviousVersion()
    commits = version.getDiff()[file]['commits']
    developer_xp = developer_count_version(previous_version)
    mean = 0

    for commit in commits:
        developer = commit.getAuthor()
        if developer in developer_xp:
            mean += developer_xp[developer]

    if len(commits) == 0:
        return 0
    return round(mean / len(commits), 2)
