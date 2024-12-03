from Objects.Version import Version


def metric_03_commit_count(file: str, version: Version) -> int:
    if file not in version.getDiff():
        return 0
    return len(version.getDiff()[file]['commits'])
