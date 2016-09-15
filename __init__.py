"""
__init__.py

Description:
    global configuration for the fitness package
"""
# ==============================================================================
# Dependencies
# ==============================================================================
# Python libraries
import logging
import os


# ==============================================================================
# Constants / Globals
# ==============================================================================
# logging
logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")
LOGGER = logging.getLogger(__name__)

# database
PACKAGE_ROOT = os.path.dirname(__file__)
DATABASE = os.path.join(PACKAGE_ROOT, "python", "database", "fitness")

# attribute import management
__all__ = [LOGGER, PACKAGE_ROOT, DATABASE]
