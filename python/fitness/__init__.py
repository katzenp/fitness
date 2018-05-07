import logging
import logging.config
import os


# ==============================================================================
# file system
# ==============================================================================
ROOT = os.path.dirname(os.path.realpath(__file__))
MAIN = os.path.join(ROOT, "main")
RESOURCES = os.path.join(ROOT, "resources")
MANAGEMENT = os.path.join(ROOT, "management")


# ==============================================================================
# logging
# ==============================================================================
LOGGING_CONFIG = os.path.join(MANAGEMENT, "logging.cfg")
logging.config.fileConfig(LOGGING_CONFIG)
LOGGER = logging.getLogger(__package__)