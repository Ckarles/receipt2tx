from .abstract import Backend, URI
from . import backend_local


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


# Mapping of supported URI protocols to backend classes.
# Update this mapping to add support for new backend types
SUPPORTED_URI_PROTOCOL_TO_BACKEND = {
    "file": backend_local.Local,
}


# List of supported URI protocols
SUPPORTED_URI_PROTOCOLS = [
    f"{uri_protocol}://" for uri_protocol in SUPPORTED_URI_PROTOCOL_TO_BACKEND.keys()
]
