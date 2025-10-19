import os
import pathlib
import tempfile
import typing as t

import pytest

from ..abstract import URI
from ..backend_local import Local

unit = pytest.mark.unit
integration = pytest.mark.integration


# --- Integration Test Fixtures ---


@pytest.fixture(scope="session")
def integration_root_dir() -> t.Generator[pathlib.Path]:
    """Create a temporary root directory for all integration tests in this session.

    This is the recommended place for session-scoped temporary directories.
    """
    # Use tempfile.TemporaryDirectory to ensure automatic cleanup
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Yield the path for the tests to use
        yield pathlib.Path(tmp_dir)


@pytest.fixture
def local_backend_fixture(
    integration_root_dir: pathlib.Path,
) -> Local:
    """Create a temporary directory for a specific test.

    Return a Local instance pointing to it.

    This ensures test isolation.
    """
    # Create a unique subdirectory for this specific test function
    test_dir = integration_root_dir / os.urandom(8).hex()
    test_dir.mkdir(parents=True, exist_ok=True)

    # Yield the backend instance
    return Local(path=test_dir)

    # Teardown (though handled by integration_root_dir cleanup, this is good practice
    # if you needed function-level cleanup)
    # Since we create unique dirs, no further action is strictly needed here.


# --- Tests ---


@unit
def test_local_from_uri_valid() -> None:
    """Unit test for the URI parsing logic."""
    raw_uri = "file:///path/to/local/dir"
    uri = URI.from_uri_raw(raw_uri)
    local_backend = Local.from_uri(uri)

    assert isinstance(local_backend, Local)
    assert local_backend.path == pathlib.Path("/path/to/local/dir")
    assert str(local_backend.path) == "/path/to/local/dir"


@unit
def test_local_from_uri_file_protocol_check() -> None:
    """Unit test to ensure the protocol is 'file' (implicit test of the URI class)."""
    raw_uri = "file:///data"
    uri = URI.from_uri_raw(raw_uri)
    assert uri.protocol == "file"
    assert uri.path == "/data"


# ----------------------------------------------------------------------
# INTEGRATION TESTS
# ----------------------------------------------------------------------


@integration
def test_list_empty_directory(local_backend_fixture: Local) -> None:
    """Test 'list' on a newly created, empty directory."""
    files = list(local_backend_fixture.list())
    assert files == []


@integration
def test_list_with_files(local_backend_fixture: Local) -> None:
    """Test 'list' correctly finds only files, ignoring subdirectories."""
    # Arrange: Create test files and a subdirectory
    file1 = local_backend_fixture.path / "image1.jpg"
    file2 = local_backend_fixture.path / "document.pdf"
    subdir = local_backend_fixture.path / "temp_data"

    file1.write_text("content1")
    file2.write_text("content2")
    subdir.mkdir()

    # Act
    files = list(local_backend_fixture.list())

    # Assert
    # We expect exactly two file paths back
    expected_files_length = 2
    assert len(files) == expected_files_length
    # Ensure both files are present and the subdir is absent
    assert file1 in files
    assert file2 in files
    assert subdir not in files


@integration
def test_fetch_single_file(local_backend_fixture: Local) -> None:
    """Test 'fetch' returns a stream with the correct content."""
    # Arrange: Create a test file
    file_name = "test_fetch.txt"
    file_path = local_backend_fixture.path / file_name
    expected_content = b"This is the content to be fetched."
    file_path.write_bytes(expected_content)

    # Act: Get the iterable of streams
    with local_backend_fixture.fetch(file_path) as stream:
        actual_content = stream.read()

        assert actual_content == expected_content
        assert (
            stream.closed is False
        )  # Check if the stream is open (caller responsibility to close)

    # NOTE: Since the `fetch` implementation uses `with open()`, the stream is closed
    # upon exiting the `with` block *inside* the `fetch` method.
    # A true streaming backend would yield an open stream/chunk,
    # but for local files, this implementation is common.
