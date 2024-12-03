from Objects.Version import Version


def metric_01_added_lines(file: str, version: Version) -> int:
    if file not in version.getDiff().keys():
        return 0

    return version.getDiff()[file]['insertions']
