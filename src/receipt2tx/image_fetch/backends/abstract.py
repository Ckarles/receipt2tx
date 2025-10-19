from abc import ABC, abstractmethod
from contextlib import contextmanager
import dataclasses
import pathlib
import typing as t


@dataclasses.dataclass
class URI:
    """A URI for a backend storage."""

    protocol: str
    path: str

    @classmethod
    def from_uri_raw(cls, uri_raw: str) -> "URI":
        try:
            protocol, path = uri_raw.split("://", 1)
        except ValueError:
            raise ValueError(
                f'Invalid URI format: "{uri_raw}" must be in the format <backend>://<path>'
            )
        return cls(
            protocol,
            path,
        )


class Backend(ABC):
    """Abstract class for a backend storage."""

    @classmethod
    @abstractmethod
    def from_uri(cls, uri: URI) -> "Backend":
        """Create a specific backend from a URI."""

    @abstractmethod
    def list(self) -> t.Iterable[pathlib.Path]:
        """List all source files in the backend directory."""

    @contextmanager
    @abstractmethod
    def fetch(self, file_path: pathlib.Path) -> t.Iterator[t.BinaryIO]:
        """Fetch a file from the backend and return it as a stream of bytes.

        Fetch has to yield streams implementing read seek and tell methods.
        Often, this means the file will have to be temporarily stored in memory or in the file system.
        """
