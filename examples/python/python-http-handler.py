"""
This file configures a logger and sent the log to a remote HTTP server.
"""

import logging
import logging.handlers

logging.basicConfig()

logger = logging.getLogger('Synchronous Logging')
http_handler = logging.handlers.HTTPHandler(
    '127.0.0.1:5000',
    '/loggers/python/http-handler?key=LIh982y87GgljahsadfklJHLIUG87g1u1e7f6eb2ee145571858e8e24',
    method='POST',
)
logger.addHandler(http_handler)

logger.setLevel(logging.DEBUG)

logger.info('This is a test log message')
exit(0)

for x in range(0, 100):
    try:
        1 / 0
    except Exception as e:
        logger.error('Error', exc_info=e, extra={'foo': 'bar'}, stack_info=True)
        logger.exception("asdf", e)


