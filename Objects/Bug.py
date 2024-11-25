from git import Commit

from Objects.Version import Version


class Bug:
    _instances = {}

    def __new__(cls, name: int, commit: Commit):
        # Use hash to check if the bug already exists
        if name not in cls._instances:
            cls._instances[name] = super(Bug, cls).__new__(cls)
        return cls._instances[name]

    def __init__(self, name: int, commit: Commit):
        self.name: int = name
        self.impacted_versions: [Version] = []
        self.commit: Commit = commit

    # Setters -----------------------------------------------------------------

    def setImpactedVersions(self, impacted_versions: [Version]) -> None:
        # Remove actual links between the bug and the versions
        for version in self.impacted_versions:
            version.removeBug(self)

        # Set the new list of impacted versions
        self.impacted_versions = impacted_versions
        self.impacted_versions.sort()

        # Add the links between the bug and the versions
        for version in self.impacted_versions:
            version.addBug(self)

    def addImpactedVersion(self, version: Version) -> None:
        if version in self.impacted_versions:
            print(f"Version {version} already in the list of impacted versions for bug {self.name}")

        self.impacted_versions.append(version)
        # Sort the list of impacted versions
        self.impacted_versions.sort()
        version.addBug(self)

    def removeImpactedVersion(self, version: Version) -> None:
        if version not in self.impacted_versions:
            print(f"Version {version} not in the list of impacted versions for bug {self.name}")

        self.impacted_versions.remove(version)
        version.removeBug(self)

    # Getters -----------------------------------------------------------------

    def getName(self) -> int:
        return self.name

    def getImpactedVersions(self) -> [Version]:
        return self.impacted_versions

    def getCommit(self) -> Commit:
        return self.commit

    # Python internal methods -------------------------------------------------

    def __str__(self) -> str:
        buffer: str = f"Hive-{self.name}"
        for version in self.impacted_versions:
            buffer += f"\n\t{version}"
        return buffer

    def __repr__(self) -> str:
        return f"Hive-{self.name}"

    def __hash__(self):
        return hash(self.name)
