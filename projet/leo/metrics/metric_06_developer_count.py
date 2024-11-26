from git import Commit

from Objects.Version import Version


def metric_06_developer_count(file: str, version: Version) -> int:
    if file not in version.getDiff():
        return 0
    authors = set()
    commit: Commit = version.getCommit()
    for commit in version.getDiff()[file]['commits']:
        authors.add(commit.author.email)
    return len(authors)
