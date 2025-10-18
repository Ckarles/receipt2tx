from abc import ABC, abstractmethod
import dataclasses


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
