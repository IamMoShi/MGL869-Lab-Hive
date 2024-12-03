from Objects.Version import Version
from projet.leo.metrics.metric_03_commit_count import metric_03_commit_count


def metric_05_commit_count_all(file: str, version: Version) -> int:
    counter: int = 0

    while version:
        counter += metric_03_commit_count(file, version)
        version = version.getPreviousVersion()
    return counter
