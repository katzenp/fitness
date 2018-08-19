# Python standard libraries
import json
import logging
import logging.config
import os


# ==============================================================================
# constants/globals
# ==============================================================================
# file system
ROOT = __file__.rsplit(os.sep, 3)[0]
BIN = os.path.join(ROOT, "bin")
CACHES = os.path.join(ROOT, "resources", "caches")
CONFIGS = os.path.join(ROOT, "resources", "configs")
TEMPLATES = os.path.join(ROOT, "resources", "templates")

# settings
SETTINGS_FILE = os.path.join(CONFIGS, "settings.json")
SETTINGS = {}
with open(SETTINGS_FILE, "r") as istream:
    SETTINGS = json.load(istream)

# logging
LOGGING_CONFIG = os.path.join(CONFIGS, "logging.cfg")
logging.config.fileConfig(LOGGING_CONFIG)
LOGGER = logging.getLogger(__package__)


# ==============================================================================
# decorators
# ==============================================================================
def decimal_places(precision=SETTINGS["precision"]):
    def _precision(func):
        def _wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return round(result, precision)
        return _wrapper
    return _precision
