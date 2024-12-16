from Objects import Version


def added_lines(version: Version) -> {str: int}:
    """
    Returns the added lines of code for each file in the version.
    """
    ans: {str: int} = {}
    commits: {"str": dict} = version.version_commits
    for commit_hash in commits:
        commit = commits[commit_hash]
        for file in commit["modified_files"]:
            file_name = file["filename"]
            if file_name not in ans:
                ans[file_name] = 0
            ans[file_name] += file["added_lines"]
    return ans
