SQLite Driver for Intake Data Catalogs
=======================================================================================

.. readme-intro

.. image:: https://github.com/catalyst-cooperative/intake-sqlite/workflows/tox-pytest/badge.svg
   :target: https://github.com/catalyst-cooperative/intake-sqlite/actions?query=workflow%3Atox-pytest
   :alt: Tox-PyTest Status

.. image:: https://img.shields.io/codecov/c/github/catalyst-cooperative/intake-sqlite?style=flat&logo=codecov
   :target: https://codecov.io/gh/catalyst-cooperative/intake-sqlite
   :alt: Codecov Test Coverage

.. image:: https://img.shields.io/readthedocs/intake-sqlite?style=flat&logo=readthedocs
   :target: https://intake-sqlite.readthedocs.io/en/latest/
   :alt: Read the Docs Build Status

.. image:: https://img.shields.io/pypi/v/intake-sqlite?style=flat&logo=python
   :target: https://pypi.org/project/intake-sqlite
   :alt: PyPI Latest Version

.. image:: https://img.shields.io/conda/vn/conda-forge/intake-sqlite?style=flat&logo=condaforge
   :target: https://anaconda.org/conda-forge/intake-sqlite
   :alt: conda-forge Version

.. image:: https://img.shields.io/pypi/pyversions/intake-sqlite?style=flat&logo=python
   :target: https://pypi.org/project/intake-sqlite
   :alt: Supported Python Versions

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black>
   :alt: Any color you want, so long as it's black.

This package provides a (very) thin wrapper around the more general `intake-sql
<https://github.com/intake/intake-sql>`__ driver, which can be used to generate `Intake
data catalogs <https://github.com/intake/intake>`__ from SQL databases.

The ``intake-sql`` driver takes an `SQL Alchemy database URL
<https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls>`__ and uses it to
connect to and extract data from the database. This works with just fine with
`SQLite databases <https://www.sqlite.org/index.html>`__, but only when the database
file is stored locally and can be referenced with a simple path.

For example this path:

.. code::

  /home/zane/code/catalyst/pudl-work/sqlite/pudl.sqlite

would correspond to this SQL Alchemy database URL:

.. code::

  sqlite:///home/zane/code/catalyst/pudl-work/sqlite/pudl.sqlite

But you can't access a remote SQLite DB this way.

Why access a remote SQLite DB?
=======================================================================================

* SQLite databases are great standalone, standardized containers for relational data,
  that can be accessed using a huge variety of tools on almost any computer platform.
  They are even accepted as an archival format by the US Library of Congress!
* Data evolves over time, and it's often useful to have easy access to several
  different versions of it, and to know exactly which version you're working with.
* Cloud object storage is extremely cheap and convenient, and makes it easy to
  publish and store historical file-based data releases.
* Managing your own bespoke local filesystem hierarchy filled with data -- and
  coordinating with colleagues so that everyone is using the same filesystem
  organizational scheme -- is a pain.
* Intake catalogs can provide easy access to metadata and let you manage data versions
  just like software versions. Installing a new version of the data catalog points you
  at the new version of the data.
* The overhead and cost associated with setting up and maintaining a database that uses
  a client-server model is relatively large compared to distributing a few files that
  change infrequently, are essentially read-only resources, and only take up a few
  gigabytes of space.

How does it work?
=======================================================================================
Rather than using an SQL Alchemy database URL to reference the SQLite DB, this intake
driver takes a local path or a remote URL, like:

* ``../pudl-work/sqlite/pudl.sqlite``
* ``https://global-power-plants.datasettes.com/global-power-plants.db``
* ``s3://cloudy-mc-cloudface-databucket/v1.2.3/mydata.db``

For local paths, it resolves the path and prepends ``sqlite://`` before handing it off
to ``intake-sql`` to do all the hard work.

For remote URLs it uses `fsspec <https://filesystem-spec.readthedocs.io/en/latest/>`__
to `cache a local copy <https://filesystem-spec.readthedocs.io/en/latest/features.html?highlight=simplecache#caching-files-locally>`__
of the database, and then gives ``intake-sql`` a database URL that points to the cached
copy.

.. code:: python

  import intake_sqlite

  gpp_cat = intake_sqlite.SQLiteCatalog(
      urlpath="https://global-power-plants.datasettes.com/global-power-plants.db",
      open_kwargs={"simplecache": {"cache_storage": "/home/zane/.cache/intake"}},
  )

  list(gpp_cat)

  # ['global-power-plants',
  #  'global-power-plants_fts',
  #  'global-power-plants_fts_config',
  #  'global-power-plants_fts_data',
  #  'global-power-plants_fts_docsize',
  #  'global-power-plants_fts_idx']

About Catalyst Cooperative
=======================================================================================
`Catalyst Cooperative <https://catalyst.coop>`__ is a small group of data
wranglers and policy wonks organized as a worker-owned cooperative consultancy.
Our goal is a more just, livable, and sustainable world. We integrate public
data and perform custom analyses to inform public policy (`Hire us!
<https://catalyst.coop/hire-catalyst>`__). Our focus is primarily on mitigating
climate change and improving electric utility regulation in the United States.

Contact Us
----------
* For general support, questions, or other conversations around the project
  that might be of interest to others, check out the
  `GitHub Discussions <https://github.com/catalyst-cooperative/pudl/discussions>`__
* If you'd like to get occasional updates about our projects
  `sign up for our email list <https://catalyst.coop/updates/>`__.
* Want to schedule a time to chat with us one-on-one? Join us for
  `Office Hours <https://calend.ly/catalyst-cooperative/pudl-office-hours>`__
* Follow us on Twitter: `@CatalystCoop <https://twitter.com/CatalystCoop>`__
* More info on our website: https://catalyst.coop
* For private communication about the project or to hire us to provide customized data
  extraction and analysis, you can email the maintainers:
  `pudl@catalyst.coop <mailto:pudl@catalyst.coop>`__
