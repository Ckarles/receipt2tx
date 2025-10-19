import pytest

from ..backend_local import Local
from .. import factory


unit = pytest.mark.unit
integration = pytest.mark.integration

# Define test cases using parametrize: (URI_input, expected_backend_type, *expected_args)
# The order in the tuple matters and aligns with the test function arguments.
test_uris = [
    # Local File URIs
    ("file:///var/my-files/sample", Local, "/var/my-files/sample"),
    (
        "file://data/in",
        Local,
        "data/in",
    ),  # Technically invalid but tests logic resilience
    ## S3 URIs
    # (
    #    "s3://my-test-bucket/images/receipts/",
    #    S3Backend,
    #    "my-test-bucket",
    #    "images/receipts/",
    # ),
    # ("s3://another-bucket", S3Backend, "another-bucket", ""),
]


@unit
@pytest.mark.parametrize("raw_uri, expected_type, expected_args", test_uris)
def test_parse_valid_uris(raw_uri, expected_type, expected_args):
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

    # elif expected_type is S3Backend:
    #     expected_bucket, expected_key = expected_args
    #     assert backend_instance.bucket == expected_bucket, (
    #         "S3 bucket name should be correctly parsed."
    #     )
    #     assert backend_instance.key_path == expected_key, (
    #         "S3 key path should be correctly parsed."
    #     )


@unit
def test_parse_invalid_format():
    """Tests error handling for missing scheme/delimiter."""
    with pytest.raises(ValueError) as excinfo:
        factory.select_backend_from_uri_raw("/home/user/data")  # Missing '://'
    assert "Invalid URI format" in str(excinfo.value)


@unit
def test_parse_unsupported_backend():
    """Tests error handling for a backend type that hasn't been implemented."""
    with pytest.raises(ValueError) as excinfo:
        factory.select_backend_from_uri_raw(
            "gcs://my-gcp-bucket/files"
        )  # 'gcs' is not supported by parse_uri
    assert "Unsupported backend" in str(excinfo.value)
