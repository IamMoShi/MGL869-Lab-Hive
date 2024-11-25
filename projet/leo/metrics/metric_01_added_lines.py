def metric_01_added_lines(file: str, version: str) -> int:
    assert version.getDiff() != dict()

    if not file in version.getDiff():
        return 0

    return version.getDiff()[file]['insertions']
