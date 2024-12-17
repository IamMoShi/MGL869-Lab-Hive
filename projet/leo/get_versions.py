from git import Repo, Commit, Tag
from configparser import ConfigParser
from re import compile, Pattern

from Objects.Version import Version


def get_versions(repository: Repo, minimal_version=(2, 0, 0)) -> [Version]:
    """
    Use the regex of the config file to get the versions of the repository
    :param minimal_version: Above this, versions will be considered as valid
    :param repository: The repository to get  versions
    :return: Versions of the repository
    """

    config = ConfigParser()
    config.read('config.ini')

    releases_regex: [str] = config["GIT"]["ReleasesRegex"].split(",")
    tags: [Tag] = repository.tags
    releases_regex: [str] = [regex.strip() for regex in releases_regex]
    releases_regex = [compile(regex) for regex in releases_regex]

    filtered_versions: [Version] = []
    for tag in tags:
        if any(regex.match(tag.name) for regex in releases_regex):
            version: str = tag.name
            version_numbers = version.split("-")[1]
            if tuple(map(int, version_numbers.split("."))) < minimal_version:
                continue
            version: Version = Version(tag, *map(int, version_numbers.split(".")))
            filtered_versions.append(version)

    build_versions_dependencies(filtered_versions)
    return filtered_versions


def found_previous_version(versions: [Version], position: int) -> Version or None:
    """
    Find the previous version of a version
    :param versions: The versions to search in (sorted by date!!!)
    :param position: The position of the version to find the previous version for in the list of versions
    :return: The previous version if found, None otherwise
    """
    version = versions[position]
    instances = version.getInstances()
    if version.id[2] != 0:
        previous_version = instances.get((version.id[0], version.id[1], version.id[2] - 1))
        if previous_version is not None:
            return previous_version
        else:
            raise ValueError("Previous version not found make sure to create all versions before calling this function")

    previous_version = versions[0]
    for v in versions:
        if v >= version:
            return previous_version
        if v > previous_version:
            previous_version = v
    return None


def build_versions_dependencies(versions: [Version]):
    """
    Build the dependencies between versions,
    Link previous versions to their next versions
    :param versions: The versions to build the dependencies for
    :return: None
    """
    versions.sort(key=lambda version: version.getDate())
    for i in range(len(versions)):
        version = versions[i]
        previous_version = found_previous_version(versions, i)
        version.setPreviousVersion(previous_version)
        print(f"Version {version.id} built !")

    versions[0].setPreviousVersion(None)
    versions[0].next_versions.remove(versions[0])

    for i in range(len(versions)):
        version = versions[i]
        version.calculate_metrics()
