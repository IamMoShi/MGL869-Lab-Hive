from configparser import ConfigParser
from os import path

from DateTime import DateTime
from git import Commit, Tag
from subprocess import run, PIPE, CompletedProcess


class Version:
    _instances = {}

    def __new__(cls, tag: Tag, a: int, b: int, c: int):
        if (a, b, c) not in cls._instances:
            cls._instances[(a, b, c)] = super(Version, cls).__new__(cls)
        return cls._instances[(a, b, c)]

    def __init__(self, tag: Tag or None, a: int, b: int, c: int):
        self.id = (a, b, c)
        self.tag: Tag = tag
        self.date: DateTime or None = tag.commit.committed_datetime
        self.previous_version: "Version" or None = None
        self.next_versions: ["Version"] = set()
        self.bugs: ["Bug"] = set()
        self.commits_logs: [Commit] = Version.git_log(self)
        self.version_commits: [Commit] = []
        self.diff: dict = dict()

    # Setters -----------------------------------------------------------------
    def setPreviousVersion(self, previous_version: "Version" or None) -> None:
        self.previous_version = previous_version
        if previous_version is not None:
            previous_version.addNextVersion(self)
            commits_logs_previous_version: [Commit] = previous_version.getCommitsLogs()
            for commit in self.commits_logs:
                if commit in commits_logs_previous_version:
                    break
                self.version_commits.append(commit)
            self.diff = self.git_diff()

    def addNextVersion(self, next_version: "Version") -> None:
        self.next_versions.add(next_version)

    def addBug(self, bug: "Bug") -> None:
        self.bugs.add(bug)

    def removeBug(self, bug: "Bug") -> None:
        self.bugs.remove(bug)

    # Getters -----------------------------------------------------------------

    def getInstances(self) -> {(int, int, int): "Version"}:
        return self._instances

    def getId(self) -> (int, int, int):
        return self.id

    def getTag(self) -> Tag:
        return self.tag

    def getCommit(self) -> Commit:
        return self.tag.commit

    def getDate(self) -> DateTime:
        if self.date is None:
            raise ValueError("Date not set")
        return self.date

    def getPreviousVersion(self) -> "Version":
        return self.previous_version

    def getNextVersions(self) -> ["Version"]:
        output: ["Version"] = list(self.next_versions)
        output.sort()
        return output

    def getRepo(self):
        return self.tag.repo

    def getBranch(self) -> str:
        branch_name: str = f"origin/branch-{self.id[0]}.{self.id[1]}"
        return branch_name

    def getCommitsLogs(self) -> [Commit]:
        return self.commits_logs

    def getVersionCommits(self) -> [Commit]:
        return self.version_commits

    def getDiff(self) -> dict:
        return self.diff

    # Python internal methods -------------------------------------------------

    def __str__(self):
        buffer: str = f"Version " + ".".join(map(str, self.id))
        for bug in self.bugs:
            buffer += f"\n\t{bug}"
        return buffer

    def __repr__(self):
        return f"V" + ".".join(map(str, self.id))

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __ne__(self, other):
        return self.id != other.id

    # Specific methods --------------------------------------------------------
    files_found: set = set()

    def git_diff(self) -> dict:
        version_commits: list[Commit] = self.getVersionCommits()

        output: dict = {str: dict}

        for commit in version_commits:
            files = dict(commit.stats.files)
            diff_commit = {file: {'insertion': 0, 'deletion': 0, 'lines': 0} for file in files}
            for file in files:
                Version.files_found.add(file)
                if file not in output:
                    output[file] = dict()
                    output[file]['insertions'] = 0
                    output[file]['deletions'] = 0
                    output[file]['lines'] = 0
                    output[file]['commits'] = []
                output[file]['insertions'] += files[file]['insertions']
                output[file]['deletions'] += files[file]['deletions']
                output[file]['lines'] += files[file]['lines']
                output[file]['commits'].append(commit)
                diff_commit[file]['insertion'] = files[file]['insertions']
                diff_commit[file]['deletion'] = files[file]['deletions']
                diff_commit[file]['lines'] = files[file]['lines']

        return output

    @staticmethod
    def git_log(version: "Version") -> [Commit]:
        # Command : git log --pretty=format:"%H" --no-patch commit.hexsha

        config = ConfigParser()
        config.read('config.ini')
        hive_git_directory = config["GIT"]["HiveGitDirectory"]
        hive_git_repo_name = config["GIT"]["HiveGitRepoName"]
        data_directory = config["GENERAL"]["DataDirectory"]

        repo_path = path.join(data_directory, hive_git_directory, hive_git_repo_name)

        commit: Commit = version.getCommit()
        command: [str] = ["git", "log", "--pretty=format:%H", "--no-patch", commit.hexsha]
        process: CompletedProcess = run(command, stdout=PIPE, stderr=PIPE, cwd=repo_path)
        commits_str: [str] = process.stdout.decode().strip().split("\n")

        output: [Commit] = []
        for c in commits_str:
            output.append(commit.repo.commit(c))

        return output

    def to_json(self):
        return {
            "id": self.id,
            "date": self.date,
            "previous_version": self.previous_version,
            "next_versions": self.next_versions,
            "bugs": self.bugs,
            "commits_logs": self.commits_logs,
            "version_commits": self.version_commits,
            "diff": self.diff
        }