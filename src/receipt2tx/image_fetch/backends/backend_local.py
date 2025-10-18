import dataclasses
import pathlib

from .abstract import Backend, URI


@dataclasses.dataclass(frozen=True)
class Local(Backend):
    """Backend to a local file system directory.

    properties:
        - path: Path to a local directory
    """

    path: pathlib.Path

    @classmethod
    def from_uri(cls, uri: URI) -> "Local":
        return cls(pathlib.Path(uri.path))
