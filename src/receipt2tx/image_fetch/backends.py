from abc import ABC, abstractmethod
import dataclasses
import pathlib


class Backend(ABC):
    """Abstract class for a backend storage."""

    # @abstractmethod
    # def list_files():
    #    pass


@dataclasses.dataclass(frozen=True)
class Local(Backend):
    """Backend to a local file system directory.

    properties:
        - path: Path to a local directory
    """

    path: pathlib.Path

    @classmethod
    def from_path(cls, path: str) -> "Local":
        return cls(pathlib.Path(path))
