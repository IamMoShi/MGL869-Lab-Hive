from Objects.Version import Version
from projet.leo.metrics.metric_06_developer_count import metric_06_developer_count


def metric_07_developer_count_all(file: str, version: Version) -> int:
    counter: int = 0
    while version:
        counter += metric_06_developer_count(file, version)
        version = version.getPreviousVersion()
    return counter
