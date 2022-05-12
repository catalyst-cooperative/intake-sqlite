"""Create an SQLite Intake catalog from all the tables in a SQLite database."""
from __future__ import annotations

import logging
from typing import Any

from intake_sql.sql_cat import SQLCatalog

import intake_sqlite

logger = logging.getLogger(__name__)

__all__ = ["SQLiteCatalog"]


class SQLiteCatalog(SQLCatalog):  # type: ignore
    """Automatically create data sources from known SQLite database tables."""

    name = "sqlite_cat"
    version = intake_sqlite.__version__

    def __init__(
        self,
        urlpath: str,
        views: bool = False,
        sql_kwargs: str | None = None,
        open_kwargs: dict[str, Any] = {},
        **kwargs: str,
    ):
        """Initialize catalog, transforming urlpath into SQLite URL for SQL Alchemy."""
        super().__init__(
            uri=intake_sqlite.urlpath_to_sqliteurl(urlpath, open_kwargs=open_kwargs),
            views=views,
            sql_kwargs=sql_kwargs,
            **kwargs,
        )
