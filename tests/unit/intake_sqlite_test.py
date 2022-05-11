"""A dummy unit test so pytest has something to do."""
import logging

import pytest

from intake_sqlite import urlpath_to_sqliteurl

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "urlpath,expected_sqliteurl",
    [
        # ("gs://intake.catalyst.coop/test/test.db", "sqlite://"),
        ("/home/zane/code/catalyst/intake-sqlite/tests/data/test.db", "sqlite://"),
    ],
)
def test_something(urlpath: str, expected_sqliteurl: str) -> None:
    """Test the dummy function from our dummy module to generate coverage.

    This function also demonstrates how to parametrize a test.

    """
    actual_sqliteurl = urlpath_to_sqliteurl(urlpath)
    logger.info(f"{urlpath=} {actual_sqliteurl=}")
    # assert actual_sqliteurl == expected_sqliteurl  # nosec: B101
