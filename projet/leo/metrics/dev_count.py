from Objects import Version


def dev_count(version: Version) -> {str: int}:
    """
    Returns the number of developers that modified each file in the version.
    """
    ans: {str: int} = {}
    dev_memory: {str, set[str]} = {}
    commits: {"str": dict} = version.version_commits

    for commit_hash in commits:
        commit = commits[commit_hash]
        for file in commit["modified_files"]:
            file_name = file["filename"]
            if file_name not in ans:
                ans[file_name] = 0
                dev_memory[file_name] = set()
            if commit["email"] not in dev_memory[file_name]:
                dev_memory[file_name].add(commit["email"])
                ans[file_name] += 1
    return ans


def dev_count_r(version: Version) -> {str: int}:
    def recursive(v: Version, ans: {str: int}, dev_memory: {str, set[str]}):
        if v is None:
            return ans
        commits: {"str": dict} = v.version_commits

        for commit_hash in commits:
            commit = commits[commit_hash]
            for file in commit["modified_files"]:
                file_name = file["filename"]
                if file_name not in ans:
                    ans[file_name] = 0
                    dev_memory[file_name] = set()
                if commit["email"] not in dev_memory[file_name]:
                    dev_memory[file_name].add(commit["email"])
                    ans[file_name] += 1

        return recursive(v.getPreviousVersion(), ans, dev_memory)

    return recursive(version, {}, {})
