"""PyTest configuration module. Defines useful fixtures, command line args."""
from __future__ import annotations

import logging
import tempfile
from collections.abc import Generator
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import sqlalchemy as sa

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def df1() -> pd.DataFrame:
    """A dataframe with a named primary key."""
    df = pd.DataFrame(
        {
            "a": np.random.rand(100).tolist(),
            "b": np.random.randint(100, size=100).tolist(),
            "c": np.random.choice(["a", "b", "c", "d"], size=100).tolist(),
        }
    )
    df.index.name = "pk"
    return df


@pytest.fixture(scope="session")
def df2() -> pd.DataFrame:
    """A dataframe with no primary key."""
    return pd.DataFrame(
        {
            "d": np.random.rand(100).tolist(),
            "e": np.random.randint(100, size=100).tolist(),
            "f": np.random.choice(["a", "b", "c", "d"], size=100).tolist(),
        }
    )


@pytest.fixture(scope="session")
def temp_db(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
) -> Generator[tuple[str, str, str], None, None]:
    """Create a temporary SQLite DB for use in testing."""
    urlpath = Path(tempfile.mkstemp(suffix=".db")[1])
    engine = sa.create_engine(f"sqlite:///{urlpath}")
    with engine.connect() as con:
        con.execute(
            """CREATE TABLE temp (
            pk BIGINT PRIMARY KEY,
            a REAL NOT NULL,
            b BIGINT NOT NULL,
            c TEXT NOT NULL);"""
        )
        con.execute(
            """CREATE TABLE temp_nopk (
            d REAL NOT NULL,
            e BIGINT NOT NULL,
            f TEXT NOT NULL);"""
        )
        df1.to_sql("temp", con=con, if_exists="append")
        df2.to_sql("temp_nopk", con=con, if_exists="append", index=False)
    try:
        yield "temp", "temp_nopk", str(urlpath)
    finally:
        if urlpath.is_file():
            urlpath.unlink()
