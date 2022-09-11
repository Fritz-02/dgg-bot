import logging

_logger = logging.getLogger("dgg-bot")
_logger.addHandler(logging.NullHandler())


def debug(msg, *args, **kwargs):
    _logger.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    _logger.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    _logger.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    _logger.error(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    _logger.critical(msg, *args, **kwargs)
