#!/usr/bin/env python
"""Setup script to make Intake SQLite installable with pip."""

from pathlib import Path

from setuptools import find_packages, setup

readme_path = Path(__file__).parent / "README.rst"
long_description = readme_path.read_text()


setup(
    name="intake-sqlite",
    description="An Intake driver to access local or remote SQLite databases by URL.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # setuptools_scm lets us automagically get package version from GitHub tags
    setup_requires=["setuptools_scm"],
    use_scm_version=True,
    author="Catalyst Cooperative",
    author_email="pudl@catalyst.coop",
    maintainer="Zane Selvans",
    maintainer_email="zane.selvans@catalyst.coop",
    url="https://github.com/catalyst-cooperative/intake-sqlite",
    project_urls={
        "Source": "https://github.com/catalyst-cooperative/intake-sqlite",
        "Documentation": "https://intake-sqlite.readthedocs.io",
        "Issue Tracker": "https://github.com/catalyst-cooperative/intake-sqlite/issues",
    },
    license="MIT",
    # Fill in search keywords that users might use to find the package
    keywords=["intake", "sqlite", "data catalog"],
    python_requires=">=3.8,<3.11",
    # In order for the dependabot to update versions, they must be listed here.
    # Use the format "pkg_name>=x,<y"
    install_requires=[
        "intake_sql>=0.3.1,<0.4",
        "fsspec>=2022.5,<2023",
    ],
    extras_require={
        "dev": [
            "black>=22,<23",  # A deterministic code formatter
            "isort>=5,<6",  # Standardized import sorting
            "tox>=3.20,<4",  # Python test environment manager
            "twine>=3.3,<5.0",  # Used to make releases to PyPI
        ],
        "docs": [
            "doc8>=0.9,<1.1",  # Ensures clean documentation formatting
            "furo>=2022.4.7",
            "sphinx>=4,<6",  # The default Python documentation redering engine
            "sphinx-autoapi>=1.8,<3",  # Generates documentation from docstrings
            "sphinx-issues>=1.2,<4.0",  # Allows references to GitHub issues
        ],
        "tests": [
            "bandit>=1.6,<2",  # Checks code for security issues
            "coverage>=5.3,<7",  # Lets us track what code is being tested
            "doc8>=0.9,<1.1",  # Ensures clean documentation formatting
            "flake8>=4,<6",  # A framework for linting & static analysis
            "flake8-builtins>=1.5,<3",  # Avoid shadowing Python built-in names
            "flake8-colors>=0.1,<0.2",  # Produce colorful error / warning output
            "flake8-docstrings>=1.5,<2",  # Ensure docstrings are formatted well
            "flake8-rst-docstrings>=0.2,<0.3",  # Allow use of ReST in docstrings
            "flake8-use-fstring>=1,<2",  # Highlight use of old-style string formatting
            "fsspec[http]",  # Extras required for our specific test cases.
            "intake>=0.6.5,<0.7",
            "mccabe>=0.6,<0.8",  # Checks that code isn't overly complicated
            "msgpack-numpy>=0.4,<0.5",  # Required to serialize Numpy arrays
            "mypy>=0.942",  # Static type checking
            "pandas>=1.4,<2",
            "pep8-naming>=0.12,<0.14",  # Require PEP8 compliant variable names
            "pre-commit>=2.9,<3",  # Allow us to run pre-commit hooks in testing
            "pydocstyle>=5.1,<7",  # Style guidelines for Python documentation
            "pytest>=6.2,<8",  # Our testing framework
            "pytest-cov>=2.10,<5.0",  # Pytest plugin for working with coverage
            "rstcheck[sphinx]>=5,<7",  # ReStructuredText linter
            "sqlalchemy>=1.3,<2",
            "tox>=3.20,<4",  # Python test environment manager
        ],
        "types": [
            "types-setuptools",
        ],
    },
    # A controlled vocabulary of tags used by the Python Package Index.
    # Make sure the license and python versions are consistent with other arguments.
    # The full list of recognized classifiers is here: https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    # Directory to search recursively for __init__.py files defining Python packages
    packages=find_packages("src"),
    # Location of the "root" package:
    package_dir={"": "src"},
    # entry_points defines interfaces to command line scripts we distribute.
    # Can also be used for other resource deployments, like intake catalogs.
    entry_points={
        "intake.drivers": [
            "sqlite = intake_sqlite.sqlite_src:SQLiteSource",
            "sqlite_auto = intake_sqlite.sqlite_src:SQLiteSourceAutoPartition",
            "sqlite_manual = intake_sqlite.sqlite_src:SQLiteSourceManualPartition",
            "sqlite_cat = intake_sqlite.sqlite_cat:SQLiteCatalog",
        ]
    },
)
