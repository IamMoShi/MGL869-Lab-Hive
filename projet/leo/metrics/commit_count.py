from Objects import Version


def commit_count(version: Version) -> {str: int}:
    """
    Returns for each file in the version the number of commits that modified it.
    """
    ans: {str: int} = {}
    commits: {"str": dict} = version.version_commits
    for commit_hash in commits:
        commit = commits[commit_hash]
        for file in commit["modified_files"]:
            file_name = file["filename"]
            if file_name not in ans:
                ans[file_name] = 0
            ans[file_name] += 1
    return ans


def commit_count_r(version: Version) -> {str: int}:
    def recursive(v: version, ans: {str: int}):
        if v is None:
            return ans
        commits: {"str": dict} = v.version_commits

        # for each commit in the version
        for commit_hash in commits:
            commit = commits[commit_hash]
            for file in commit["modified_files"]:
                file_name = file["filename"]
                if file_name not in ans:
                    ans[file_name] = 0
                ans[file_name] += 1

        # for each previous version
        return recursive(v.getPreviousVersion(), ans)

    return recursive(version, {})


def commit_bug_count(version: Version, keywords=("fix", "bug", "error", "mistake", "patch")) -> {str: int}:
    """
    Returns for each file in the version the number of commits that modified it.
    """
    ans: {str: int} = {}
    commits: {"str": dict} = version.version_commits
    for commit_hash in commits:
        commit = commits[commit_hash]
        for file in commit["modified_files"]:
            file_name = file["filename"]
            if file_name not in ans:
                ans[file_name] = 0
            if any(keyword in commit["msg"].lower() for keyword in keywords):
                ans[file_name] += 1
    return ans

