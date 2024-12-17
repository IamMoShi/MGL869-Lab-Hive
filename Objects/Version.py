import pickle

from DateTime import DateTime
from git import Commit, Tag, Repo
import pydriller
import projet.leo.metrics as my_metrics

from projet.leo.extract_data import extract_data


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
        self.version_commits: {"str": dict} = {}
        self.metrics: {str: {str: float}} = {}

    # Setters -----------------------------------------------------------------
    def setPreviousVersion(self, previous_version: "Version" or None) -> None:
        self.previous_version = previous_version
        if previous_version is not None:
            previous_version.addNextVersion(self)
            self.version_commits = {}
            print(f"Building version {self.id}, previous version is {previous_version.id}")
            if previous_version != self:
                pydriller_repo = pydriller.Repository(self.getRepo().working_dir, from_tag=previous_version.getTag().name,
                                                      to_tag=self.getTag().name)
            else:
                pydriller_repo = pydriller.Repository(self.getRepo().working_dir,
                                                      to_tag=self.getTag().name)
            for commit in pydriller_repo.traverse_commits():
                self.version_commits[commit.hash] = extract_data(commit)

    def calculate_metrics(self):
        """
        Run after creating all versions to calculate metrics.s
        """
        # Calculate metrics
        self.metrics["added_lines"] = my_metrics.added_lines(self)
        self.metrics["deleted_lines"] = my_metrics.deleted_lines(self)
        self.metrics["commit_count"] = my_metrics.commit_count(self)
        self.metrics["commit_count_r"] = my_metrics.commit_count_r(self)
        self.metrics["commit_bug_count"] = my_metrics.commit_bug_count(self)
        self.metrics["dev_count"] = my_metrics.dev_count(self)
        self.metrics["dev_count_r"] = my_metrics.dev_count_r(self)
        self.metrics["mean_time"] = my_metrics.mean_time(self)
        self.metrics["mean_time_r"] = my_metrics.mean_time_r(self)
        self.metrics["commit_bug_count"] = my_metrics.commit_bug_count(self)
        self.metrics["dev_mean_exp"] = my_metrics.dev_mean_exp(self)
        self.metrics["dev_min_exp"] = my_metrics.dev_min_exp(self)
        self.metrics["commit_comment_changed"], self.metrics["commit_comment_unchanged"] = my_metrics.commit_comment(self)


    def addNextVersion(self, next_version: "Version") -> None:
        self.next_versions.add(next_version)

    # Getters -----------------------------------------------------------------

    def getInstances(self) -> {(int, int, int): "Version"}:
        return self._instances

    def getId(self) -> (int, int, int):
        return self.id

    # ---------------------------------
    # Git methods ---------------------

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

    def getRepo(self) -> Repo:
        return self.tag.repo

    def getBranch(self) -> str:
        branch_name: str = f"origin/branch-{self.id[0]}.{self.id[1]}"
        return branch_name

    # ---------------------------------
    # Version categorization ----------

    def isPatch(self) -> bool:
        identifier = self.id
        return identifier[2] != 0

    def isMinor(self) -> bool:
        identifier = self.id
        return identifier[2] == 0 and identifier[1] != 0

    def isMajor(self) -> bool:
        identifier = self.id
        return identifier[2] == 0 and identifier[1] == 0

    # Python internal methods -------------------------------------------------

    # ---------------------------------
    # Representation methods ----------

    def __str__(self):
        buffer: str = f"Version " + ".".join(map(str, self.id))
        return buffer

    def __repr__(self):
        return f"V" + ".".join(map(str, self.id))

    def __hash__(self):
        return hash(self.id)

    # ---------------------------------
    # Comparison methods --------------

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

    # ---------------------------------
    # Class methods -------------------

    @classmethod
    def getVersion(cls, identifier: (int, int, int)) -> "Version":
        return cls._instances[identifier]

    # Sauvegarder les instances de la classe Version
    @classmethod
    def save_versions(cls, file_path):
        # Accéder à toutes les instances via Version._instances
        with open(file_path, 'wb') as f:
            pickle.dump(cls._instances, f)
        print(f"Instances saved to {file_path}")

    # Charger les instances de la classe Version
    @classmethod
    def load_versions(cls, file_path):
        with open(file_path, 'rb') as f:
            loaded_instances = pickle.load(f)

        print(f"Instances loaded from {file_path}")
