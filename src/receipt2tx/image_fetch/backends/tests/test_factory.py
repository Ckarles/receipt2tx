import pytest

from .. import factory
from ..backend_local import Local

unit = pytest.mark.unit
integration = pytest.mark.integration

test_uris = [
    # Local File URIs
    ("file:///var/my-files/sample", Local, "/var/my-files/sample"),
    (
        "file://data/in",
        Local,
        "data/in",
    ),  # Technically invalid but tests logic resilience
]


@unit
@pytest.mark.parametrize(("raw_uri", "expected_type", "expected_args"), test_uris)
def test_parse_valid_uris(
    raw_uri: str,
    expected_type: type,
    expected_args: str,
) -> None:
    """Tests successful parsing of known backend URIs."""
    # 1. ACT: Call the function
    backend = factory.select_backend_from_uri_raw(raw_uri)

    # 2. ASSERT: Check the returned object type
    assert isinstance(backend, expected_type)

    # 3. ASSERT: Check the extracted arguments based on type
    if type(backend) is Local:
        expected_path = expected_args
        assert str(backend.path) == expected_path, (
            "Local path should be correctly parsed."
        )


@unit
def test_parse_invalid_format() -> None:
    """Tests error handling for missing scheme/delimiter."""
    with pytest.raises(ValueError, match="Invalid URI format"):
        factory.select_backend_from_uri_raw("/home/user/data")  # Missing '://'


@unit
def test_parse_unsupported_backend() -> None:
    """Tests error handling for a backend type that hasn't been implemented."""
    with pytest.raises(ValueError, match="Unsupported backend"):
        factory.select_backend_from_uri_raw(
            "gcs://my-gcp-bucket/files",
        )  # 'gcs' is not supported by parse_uri
