from git import Repo

from Objects.Version import Version
from projet.leo.get_versions import get_versions

repository: Repo = Repo("data/hive_data/hiveRepo/")

versions: [Version] = get_versions(repository)
# diff_between_2_versions(versions[-2], versions[-1])


