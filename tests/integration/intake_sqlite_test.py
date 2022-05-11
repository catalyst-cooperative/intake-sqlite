"""A dummy integration test so pytest has something to do."""
import logging

# from intake_sqlite import SQLiteCatalog, SQLiteSource

logger = logging.getLogger(__name__)


def test_sqlite_source() -> None:
    """Need to test basic ability to create and access an SQLiteSource."""
    pass


def test_sqlite_catalog() -> None:
    """Need to test basic ability to create and access an SQLiteCatalog."""
    pass
