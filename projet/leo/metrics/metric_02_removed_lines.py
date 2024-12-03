from Objects.Version import Version


def metric_02_removed_lines(file: str, version: Version) -> int:
    if file not in version.getDiff():
        return 0

    return version.getDiff()[file]['deletions']
