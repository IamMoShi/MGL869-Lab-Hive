from git import Commit
from ipywidgets import Datetime

from Objects.Version import Version


class File:
    _instances = {}

    def __init__(self, path: str, version: Version):
        self.identifiant: int = len(self._instances)
        self.path: str = path
        self.version: Version = version

    # Setters -----------------------------------------------------------------

    # Getters -----------------------------------------------------------------

    # Python internal methods -------------------------------------------------

    def __str__(self) -> str:
        return self.version.__repr__() + "/" + self.path

    def __repr__(self) -> str:
        return self.version.__repr__() + "/" + self.path
