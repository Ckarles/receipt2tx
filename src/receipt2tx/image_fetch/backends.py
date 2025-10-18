from abc import ABC, abstractmethod
import dataclasses
import pathlib


@dataclasses.dataclass
class URI:
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


def select_backend_from_uri_raw(uri_raw: str) -> Backend:
    """Return the appropriate backend for a given raw URI.

    raises ValueError if the URI is invalid or the backend type is not supported.
    """

    uri = URI.from_uri_raw(uri_raw)

    try:
        backend = SUPPORTED_URI_PROTOCOL_TO_BACKEND[uri.protocol]
    except KeyError:
        raise ValueError(
            f'Unsupported backend type: "{uri.protocol}", supported backends: {list(SUPPORTED_URI_PROTOCOL_TO_BACKEND.keys())}'
        )

    return backend.from_uri(uri)


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


# Mapping of supported URI protocols to backend classes.
# Update this mapping to add support for new backend types
SUPPORTED_URI_PROTOCOL_TO_BACKEND = {
    "file": Local,
}
