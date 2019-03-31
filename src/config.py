import logging
import os

from _version import VERSION

DEFAULT_PORT = 9563

logger = logging.getLogger(__name__)


class Config():
    def __init__(self):
        self.kibana_url = os.getenv('KIBANA_URL')
        self.listen_port = os.getenv('PORT', DEFAULT_PORT)
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.version = VERSION

        numeric_level = getattr(logging, self.log_level.upper(), None)
        if not isinstance(numeric_level, int):
            logger.critical('Invalid log level: %s' % log_level)
            raise ValueError('Invalid log level: %s. Must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL.')
        logging.basicConfig(level=numeric_level)

        if not self.kibana_url:
            logger.critical('The Kibana URL is required.')
            raise ValueError('The Kibana URL cannot be empty.')

    def description(self):
        config_list = [
            ('Kibana URL:', self.kibana_url),
            ('Listen port:', self.listen_port),
            ('Log level:', self.log_level)
        ]
        max_length = max(map(lambda x: len(x[0]), config_list))
        desc = '== CONFIGURATION ==\n'
        line_template = "%-" + str(max_length) + "s\t%s\n"
        for line in config_list:
            desc += (line_template % line)
        return desc