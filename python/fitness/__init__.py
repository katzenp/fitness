import os

PACKAGE_NAME = "fitness"
PACKAGE_ROOT = os.path.join(
    __file__.split(PACKAGE_NAME, 1)[0],
    PACKAGE_NAME
)

SETTINGS = os.path.join(PACKAGE_ROOT, "settings.json")
LOGGING_CONFIG = os.path.join(PACKAGE_ROOT, "logging.cfg")