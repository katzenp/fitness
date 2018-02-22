import logging
import logging.config

logging.config.fileConfig('logging.cfg')

# create logger
LOGGER = logging.getLogger('fitness')
