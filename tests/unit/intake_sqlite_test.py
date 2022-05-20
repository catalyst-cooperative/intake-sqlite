"""SQLite Intake Catalog unit tests."""
from __future__ import annotations

import logging
from pathlib import Path

import pytest

from intake_sqlite import urlpath_to_sqliteurl

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

BAD_FILES: list[tuple[str, type[Exception]]] = [
    ("database.wtf", ValueError),
    ("dbdump.sql", ValueError),
    ("nonexistent.db", ValueError),
    ("nonexistent.sqlite", ValueError),
]

BAD_URLS: list[tuple[str, type[Exception]]] = [
    ("https://catalyst.coop/pudl.wtf", ValueError),
    ("s3://catalyst.coop/pudl.dude", ValueError),
    ("gs://catalyst.coop/pudl.sql", ValueError),
    ("wtftp://catalyst.coop/pudl.sqlite", ValueError),
    ("wtftp://catalyst.coop/pudl.db", ValueError),
]


@pytest.mark.parametrize("filename,exc", BAD_FILES)
def test_bad_filenames(filename: str, exc: type[Exception], tmp_path: Path) -> None:
    """Test for failure on bad or non-existent files."""
    urlpath = tmp_path / filename
    with pytest.raises(exc):
        urlpath_to_sqliteurl(str(urlpath))


@pytest.mark.parametrize("dirname,exc", BAD_FILES)
def test_bad_dirnames(dirname: str, exc: type[Exception], tmp_path: Path) -> None:
    """Test for failure when path points to a directory, not a file."""
    urlpath = tmp_path / dirname
    urlpath.mkdir()
    with pytest.raises(exc):
        urlpath_to_sqliteurl(str(urlpath))


@pytest.mark.parametrize("url,exc", BAD_URLS)
def test_bad_urls(url: str, exc: type[Exception]) -> None:
    """Test for failure when we get a bad URL."""
    with pytest.raises(exc):
        urlpath_to_sqliteurl(url)


def test_local_path_to_sqliteurl() -> None:
    """Test our transformation of paths/URLs into SQL Alchemy URLs."""
    expected_local_url = f"sqlite:///{DATA_DIR / 'test.db'}"
    test_db_path = DATA_DIR / "test.db"
    actual_local_url = urlpath_to_sqliteurl(str(test_db_path))
    assert actual_local_url == expected_local_url  # nosec: B101


# Note: There's no remote URL unit test for a working input to urlpath_to_sqliteurl()
# because it's exercised in the integration tests, and there's no way to know what the
# local path to the cached file will be since it uses a hash (of the URL?) as the
# filename.
