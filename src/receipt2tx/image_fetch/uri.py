from . import backends


def parse_URI(uri: str) -> backends.Backend:
    """Parse a URI and return the appropriate backend.

    raises ValueError if the URI is invalid or the backend type is not supported.
    """
    try:
        [backend_type, path] = uri.split("://", 1)
    except ValueError:
        raise ValueError(f"Invalid URI format: {uri}")
    if backend_type == "file":
        return backends.Local.from_path(path)

    raise ValueError(f"Unsupported backend type: {backend_type}")
