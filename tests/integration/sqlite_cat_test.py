"""SQLite Catalog integration tests."""
from __future__ import annotations

import logging

import pandas as pd
from pandas.testing import assert_frame_equal

from intake_sqlite import SQLiteCatalog

logger = logging.getLogger(__name__)


def test_local_sqlite_catalog(
    temp_db: tuple[str, str, str],
    df1: pd.DataFrame,
    df2: pd.DataFrame,
) -> None:
    """Test reading tables from a local SQLite catalog."""
    table, table_nopk, urlpath = temp_db
    cat = SQLiteCatalog(urlpath)
    assert table in cat  # nosec: B101
    assert table_nopk in cat  # nosec: B101
    actual_pk = getattr(cat, table).read()
    assert_frame_equal(df1, actual_pk)
    actual_nopk = getattr(cat, table_nopk).read()
    assert_frame_equal(df2, actual_nopk)


def test_remote_sqlite_catalog() -> None:
    """Test ability to create and access a remote SQLiteCatalog."""
    gpp_cat = SQLiteCatalog(
        urlpath="https://global-power-plants.datasettes.com/global-power-plants.db",
    )
    assert "global-power-plants" in gpp_cat  # nosec: B101
