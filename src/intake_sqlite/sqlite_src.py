"""SQLite Intake driver classes."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import fsspec
from intake_sql import SQLSource, SQLSourceAutoPartition, SQLSourceManualPartition

import intake_sqlite

logger = logging.getLogger(__name__)

SQLITE_SUFFIXES = (".db", ".sqlite")


__all__ = [
    "SQLiteSource",
    "SQLiteSourceAutoPartition",
    "SQLiteSourceManualPartition",
    "urlpath_to_sqliteurl",
]


class SQLiteSource(SQLSource):  # type: ignore
    """Read the full results of an SQL query into a dataframe.

    Args:
        urlpath: A local path or :mod:`fsspec` readable URL pointing to a SQLite
            database.
        sql_expr: Query expression to pass to the SQLite database backend.
        sql_kwargs: Additional arguments to pass in to :func:`pandas.read_sql`.
        metadata: Arbitrary metadata dictionary associated with the data source.
        open_kwargs: Additional arguments to pass to :func:`fsspec.open_local`

    """

    name = "sqlite"
    version = intake_sqlite.__version__
    container = "dataframe"
    partition_access = True

    def __init__(
        self,
        urlpath: str,
        sql_expr: str,
        sql_kwargs: dict[str, Any] = {},
        metadata: dict[str, Any] = {},
        open_kwargs: dict[str, Any] = {},
    ):
        """Initialize the class, transforming remote URL path to a local file path."""
        super().__init__(
            uri=urlpath_to_sqliteurl(urlpath, open_kwargs=open_kwargs),
            sql_expr=sql_expr,
            sql_kwargs=sql_kwargs,
            metadata=metadata,
        )


class SQLiteSourceAutoPartition(SQLSourceAutoPartition):  # type: ignore
    """SQLite Table reader with automatic partitioning.

    Args:
        urlpath: A local path or :mod:`fsspec` readable URL pointing to a SQLite
            database.
        table: Name of the table to read from the database.
        index: Name of the column to use for partitioning and as the index of the
            resulting dataframe.
        sql_kwargs: Additional arguments to pass to :func:`dask.dataframe.read_sql`.
        metadata: Arbitrary metadata dictionary associated with the data source.
        open_kwargs: Additional arguments to pass to :func:`fsspec.open_local`
    """

    name = "sqlite_auto"
    version = intake_sqlite.__version__
    container = "dataframe"
    partition_access = True

    def __init__(
        self,
        urlpath: str,
        table: str,
        index: str,
        sql_kwargs: dict[str, Any] = {},
        metadata: dict[str, Any] = {},
        open_kwargs: dict[str, Any] = {},
    ):
        """Initialize the class, transforming remote URL path to a local file path."""
        super().__init__(
            uri=urlpath_to_sqliteurl(urlpath, open_kwargs=open_kwargs),
            table=table,
            index=index,
            sql_kwargs=sql_kwargs,
            metadata=metadata,
        )


class SQLiteSourceManualPartition(SQLSourceManualPartition):  # type: ignore
    """SQLite expression reader with explicit partitioning.

    Args:
        urlpath: A local path or :mod:`fsspec` readable URL pointing to a SQLite
            database.
        sql_expr: Query expression to pass to the SQLite database backend.
        where_values: list of str or list of values/tuples
            Either a set of explicit partitioning statements (e.g.,
            `"WHERE index_col < 50"`...) or pairs of valued to be entered into
            where_template, if using
        where_template: str (optional)
            Template for generating partition selection clauses, using the
            values from where_values, e.g.,
            `"WHERE index_col >= {} AND index_col < {}"`
        sql_kwargs: Additional arguments to pass to :func:`dask.dataframe.read_sql`.
        metadata: Arbitrary metadata dictionary associated with the data source.
        open_kwargs: Additional arguments to pass to :func:`fsspec.open_local`
    """

    name = "sqlite_manual"
    version = intake_sqlite.__version__
    container = "dataframe"
    partition_access = True

    def __init__(
        self,
        urlpath: str,
        sql_expr: str,
        where_values: list[Any],
        where_template: str | None = None,
        sql_kwargs: dict[str, Any] = {},
        metadata: dict[str, Any] = {},
        open_kwargs: dict[str, Any] = {},
    ):
        """Initialize the class, transforming remote URL path to a local file path."""
        super().__init__(
            uri=urlpath_to_sqliteurl(urlpath, open_kwargs=open_kwargs),
            sql_expr=sql_expr,
            where_values=where_values,
            where_template=where_template,
            sql_kwargs=sql_kwargs,
            metadata=metadata,
        )


def urlpath_to_sqliteurl(urlpath: str, open_kwargs: dict[str, Any] = {}) -> str:
    """Transform a file path or URL into a local SQLite URL."""
    parsed = urlparse(urlpath)
    p = Path(parsed.path)
    if p.suffix not in SQLITE_SUFFIXES:
        raise ValueError(
            f"Expected a SQLite file path ending in one of: {SQLITE_SUFFIXES} "
            f"but got: {p.name}"
        )
    if parsed.scheme != "" and parsed.scheme not in fsspec.available_protocols():
        raise ValueError(f"URL protocol {parsed.scheme} is not supported by fsspec.")
    if parsed.scheme == "" and not p.is_file():
        raise ValueError(f"Local path {p} is not a file!")
    # At this point we know that EITHER:
    # * urlpath is a URL supported by fsspec that looks like an SQLite file OR
    # * p is a local file that looks like an SQLite file
    if parsed.scheme == "":
        # Absolute path to the local SQLite DB:
        local_db_path = p.resolve()
    else:
        # Absolute path to the locally cached SQLite DB:
        local_db_path = fsspec.open_local("simplecache::" + urlpath, **open_kwargs)
    return f"sqlite:///{local_db_path}"
