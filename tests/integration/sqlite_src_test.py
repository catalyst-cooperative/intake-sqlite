"""SQLite Intake Source integration tests."""
from __future__ import annotations

import logging

import pandas as pd
from pandas.testing import assert_frame_equal

from intake_sqlite import (
    SQLiteSource,
    SQLiteSourceAutoPartition,
    SQLiteSourceManualPartition,
)

logger = logging.getLogger(__name__)


def test_temp_db_fixture(temp_db: tuple[str, str, str], df1: pd.DataFrame) -> None:
    """Make sure a direct read from the temp DB works."""
    table, table_nopk, urlpath = temp_db
    actual = pd.read_sql(table, f"sqlite:///{urlpath}", index_col="pk")
    assert_frame_equal(df1, actual)


def test_simple_src(temp_db: tuple[str, str, str], df1: pd.DataFrame) -> None:
    """Test simple table read from the SQLite catalog."""
    table, table_nopk, urlpath = temp_db
    actual = SQLiteSource(urlpath, table, sql_kwargs=dict(index_col="pk")).read()
    assert_frame_equal(df1, actual)


def test_auto_src_partition(temp_db: tuple[str, str, str], df1: pd.DataFrame) -> None:
    """Test automatic partitioning of table."""
    table, table_nopk, urlpath = temp_db
    s = SQLiteSourceAutoPartition(
        urlpath, table, index="pk", sql_kwargs=dict(npartitions=2)
    )
    assert s.discover()["npartitions"] == 2  # nosec: B101
    assert s.to_dask().npartitions == 2  # nosec: B101
    actual = s.read()
    assert_frame_equal(df1, actual)


def test_manual_src_partition(temp_db: tuple[str, str, str], df1: pd.DataFrame) -> None:
    """Test manual partitioning of table."""
    table, table_nopk, urlpath = temp_db
    table, table_nopk, urlpath = temp_db
    s = SQLiteSourceManualPartition(
        urlpath,
        "SELECT * FROM " + table,  # nosec: B608
        where_values=["WHERE pk < 20", "WHERE pk >= 20"],
        sql_kwargs=dict(index_col="pk"),
    )
    assert s.discover()["npartitions"] == 2  # nosec: B101
    assert s.to_dask().npartitions == 2  # nosec: B101
    actual = s.read()
    assert_frame_equal(df1, actual)


def test_remote_sqlite_source() -> None:
    """Test ability to create and access remote SQLiteSource."""
    gpp_src = SQLiteSource(
        urlpath="https://global-power-plants.datasettes.com/global-power-plants.db",
        sql_expr="SELECT * FROM 'global-power-plants'",
    )
    df = gpp_src.read()
    assert df.shape == (34936, 36)  # nosec: B101
