"""A dummy unit test so pytest has something to do."""
import logging
from pathlib import Path

from intake_sqlite import urlpath_to_sqliteurl

logger = logging.getLogger(__name__)

TEST_DIR = Path(__file__).parent.parent.resolve()


def test_urlpath_to_sqliteurl() -> None:
    """Test our transformation of paths/URLs into SQL Alchemy URLs."""
    expected_local_url = "sqlite:///" + str(TEST_DIR / "data/test.db")
    test_db_path = TEST_DIR / "data/test.db"
    actual_local_url = urlpath_to_sqliteurl(str(test_db_path))
    assert actual_local_url == expected_local_url  # nosec: B101
