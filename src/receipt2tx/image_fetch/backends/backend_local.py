"""Backend to a local file system directory."""

import dataclasses
import pathlib
import typing as t
from contextlib import contextmanager

from .abstract import URI, Backend


@dataclasses.dataclass(frozen=True)
class Local(Backend):
    """Backend to a local file system directory.

    properties:
        - path: Path to a local directory
    """

    path: pathlib.Path

    @classmethod
    def from_uri(cls, uri: URI) -> Local:
        """Create a Local backend from a URI."""
        return cls(pathlib.Path(uri.path))

    def list(self) -> t.Iterator[pathlib.Path]:
        """List all source files in the backend directory.

        Only returns files, not subdirectories.
        """
        for path in self.path.iterdir():
            if path.is_file():
                yield path

    @contextmanager
    def fetch(self, file_path: pathlib.Path) -> t.Iterator[t.BinaryIO]:
        """Fetch a file from the backend and return it as a stream of bytes."""
        with file_path.open("rb") as f:
            yield f
