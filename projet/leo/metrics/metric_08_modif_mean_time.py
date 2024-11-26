from git import Commit

from Objects.Version import Version


def get_commits_changed_file(file: str, version: Version) -> list:
    if file not in version.getDiff():
        return []
    return version.getDiff()[file]['commits']


def metric_08_modif_mean_time(file: str, version: Version) -> float:
    # The average time between each two changes to file F in version V.
    # If in version V, there are three commits c1, c2, c3 that modified file F,
    # the average time is the mean of the time between "c1 and c2" and
    # between "c2 and c3".
    commits: set[Commit] = set(get_commits_changed_file(file, version))

    if len(commits) == 0:
        return 0.0
    elif len(commits) == 1:
        return 0.0

    commits: list[Commit] = sorted(commits, key=lambda x: x.committed_date)
    mean_time: float = 0.0
    for i in range(1, len(commits)):
        mean_time += commits[i].committed_date - commits[i - 1].committed_date
    mean_time = mean_time / (len(commits) - 1)
    # Convert the mean time from seconds to days
    mean_time = mean_time / (60 * 60 * 24)
    return round(mean_time, 1)
