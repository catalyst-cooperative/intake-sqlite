"""A dummy integration test so pytest has something to do."""
import logging

from intake_sqlite import SQLiteCatalog, SQLiteSource

logger = logging.getLogger(__name__)


def test_sqlite_source() -> None:
    """Need to test basic ability to create and access an SQLiteSource."""
    gpp_src = SQLiteSource(
        urlpath="https://global-power-plants.datasettes.com/global-power-plants.db",
        sql_expr="SELECT * FROM 'global-power-plants'",
    )
    df = gpp_src.read()
    assert df.shape == (34936, 36)  # nosec: B101


def test_sqlite_catalog() -> None:
    """Test basic ability to create and access a SQLiteCatalog."""
    gpp_cat = SQLiteCatalog(
        urlpath="https://global-power-plants.datasettes.com/global-power-plants.db",
    )
    assert list(gpp_cat)[0] == "global-power-plants"  # nosec: B101
