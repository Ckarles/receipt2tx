"""Factory to create backends from raw URIs."""

import typing as t

from . import backend_local
from .abstract import URI, Backend

# Mapping of supported URI protocols to backend classes.
# Update this mapping to add support for new backend types
SUPPORTED_URI_PROTOCOL_TO_BACKEND = {
    "file": backend_local.Local,
}


# List of supported URI protocols
SUPPORTED_URI_PROTOCOLS = [
    f"{uri_protocol}://" for uri_protocol in SUPPORTED_URI_PROTOCOL_TO_BACKEND
]

UriRaw = t.Annotated[str, "URI in the form <protocol>://<path>"]


def select_backend_from_uri_raw(uri_raw: UriRaw) -> Backend:
    """Return the appropriate backend for a given raw URI.

    raises ValueError if the URI is invalid or the backend type is not supported.
    """
    uri = URI.from_uri_raw(uri_raw)

    try:
        backend = SUPPORTED_URI_PROTOCOL_TO_BACKEND[uri.protocol]
    except KeyError as e:
        error_message = (
            f'Unsupported backend type: "{uri.protocol}", '
            f"supported backends: {SUPPORTED_URI_PROTOCOLS}"
        )
        raise ValueError(error_message) from e

    return backend.from_uri(uri)
