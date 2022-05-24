=======================================================================================
Intake SQLite Release Notes
=======================================================================================

.. _release-v0-1-1:

---------------------------------------------------------------------------------------
0.1.1 (2022-05-24)
---------------------------------------------------------------------------------------

What's New?
^^^^^^^^^^^
* Removed the misplaced and unused ``src/package_data`` directory, which was showing up
  as a separate package alongside ``src/intake_sqlite`` rather than being contained
  within the main package directory.

.. _release-v0-1-0:

---------------------------------------------------------------------------------------
0.1.0 (2022-05-20)
---------------------------------------------------------------------------------------

What's New?
^^^^^^^^^^^
This is a first draft of an :mod:`intake` data catalog driver for SQLite databases.  It
wraps the more general :mod:`intake_sql` driver and allows remote SQLite databases to be
transparently downloaded and cached locally using :mod:`fsspec`. Used in conjunction
with cloud object storage or other durable network storage with well defined versions
encoded in the URL, it will facilitate distribution of read-only, file-based, versioned
relational databases.

Known Issues
^^^^^^^^^^^^
* Code is currently based on the most recent version of :mod:`intake_sql` repository,
  which hasn't yet been published as a release.
* We need more example use cases in the README.
* Note that you'll need to install filesystem specific extras, or :mod:`fsspec` won't
  know how to work with them.
* Use of the ``simplecache::`` method is currently hard-coded. Is this appropriate?
* Additional test cases are required to exercise the
  :class:`intake_sqlite.SQLiteSourceManualPartition` and
  :class:`intake_sqlite.SQLiteSourceAutoPartition` classes.
