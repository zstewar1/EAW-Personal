import logging

loggers = set()
handlers = set()

level = logging.CRITICAL

def get_logger(name):
    "Not Idempotent -- Don't Call Twice"
    logger = logging.getLogger(name)
    logger.setLevel(level)

    loggers.add(logger)

    logging_handler = logging.StreamHandler()
    logging_handler.setLevel(level)

    handlers.add(logging_handler)

    logging_formatter = logging.Formatter('%(levelname)s %(message)s')

    logging_handler.setFormatter(logging_formatter)
    logger.addHandler(logging_handler)

    return logger

def set_levels(lvl):
    global level
    level = lvl

    for logger in loggers:
        logger.setLevel(level)
    for handler in handlers:
        handler.setLevel(level)
