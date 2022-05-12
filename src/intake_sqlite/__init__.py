"""A template repository for a Python package created by Catalyst Cooperative."""
import logging

import pkg_resources

__version__: str = pkg_resources.get_distribution("intake-sqlite").version

from intake_sqlite.sqlite_cat import *  # noqa: F403,F401
from intake_sqlite.sqlite_src import *  # noqa: F403,F401

__author__ = "Catalyst Cooperative"
__contact__ = "pudl@catalyst.coop"
__maintainer__ = "Zane Selvans"
__maintainer_email__ = "zane.selvans@catalyst.coop"
__license__ = "MIT License"
__docformat__ = "restructuredtext en"
__description__ = "An Intake driver to access local or remote SQLite databases by URL."
__projecturl__ = "https://github.com/catalyst-cooperative/intake-sqlite"
__downloadurl__ = "https://github.com/catalyst-cooperative/intake-sqlite"

# Create a root logger for use anywhere within the package.
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
