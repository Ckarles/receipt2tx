"""Abstract classes for backend storage implementations."""

import dataclasses
import typing as t
from abc import ABC, abstractmethod
from contextlib import contextmanager


@dataclasses.dataclass
class URI:
    """A URI for a backend storage."""

    protocol: str
    path: str

    @classmethod
    def from_uri_raw(cls, uri_raw: str) -> URI:
        """Parse a raw URI string into a URI object."""
        try:
            protocol, path = uri_raw.split("://", 1)
        except ValueError as e:
            error_message = (
                f'Invalid URI format: "{uri_raw}" '
                f"must be in the format <backend>://<path>"
            )
            raise ValueError(error_message) from e
        return cls(
            protocol,
            path,
        )


class Backend[T_BackendFile](ABC):
    """Abstract class for a backend storage."""

    @classmethod
    @abstractmethod
    def from_uri(cls, uri: URI) -> Backend:
        """Create a specific backend from a URI."""

    @abstractmethod
    def list(self) -> t.Iterable[T_BackendFile]:
        """List all source files in the backend directory."""

    @contextmanager
    @abstractmethod
    def fetch(self, file_path: T_BackendFile) -> t.Iterator[t.BinaryIO]:
        """Fetch a file from the backend and return it as a stream of bytes.

        Fetch has to yield streams implementing read seek and tell methods.
        Often, this means the file will have to be temporarily stored in
        memory or in the file system.
        """
