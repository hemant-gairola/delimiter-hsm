#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

import logging
import os
import threading

from src.config import get_config
from src.utils import constants

config = get_config()

LOG_FILE_PATH = config["logging"]["file_location"]
LOG_FILE_NAME = config["logging"]["file_name"]
LOG_LEVEL = config["logging"]["log_level"]

_lock = threading.Lock()

log_level = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "TRACE": constants.TRACE,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}


class AppLogger(logging.Logger):
    """
    App Logger Class which extends logging.Logger
    """

    def __init__(self, level=logging.NOTSET):
        super().__init__(name="Mongo Unload Service", level=level)

    def trace(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'TRACE'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.trace("Houston, we have a %s", "bit of a problem", exc_info=1)
        """
        if self.isEnabledFor(constants.TRACE):
            self._log(constants.TRACE, msg, args, **kwargs)


class Singleton(type):
    """
    Singleton Meta Class
    """

    __instances = {}

    def __call__(cls, *args, **kwargs):
        global _lock
        with _lock:
            if cls not in cls.__instances:
                cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


class AppFileHandler(logging.FileHandler):
    """
    AppFileHandler class to extend logging.FileHandler
    """

    def __init__(
        self, filename, mode="a", encoding=None, delay=False, errors=None
    ):  # noqa
        directory = os.path.dirname(filename)
        os.makedirs(directory, exist_ok=True)
        super().__init__(filename, mode, encoding, delay, errors)


class Logger(metaclass=Singleton):
    """
    Logger class that will be a Singleton class
    """

    def __init__(self):
        logging.addLevelName(constants.TRACE, "TRACE")
        self.logger = AppLogger()
        log_formatter = logging.Formatter(
            constants.FORMATTER, datefmt=constants.DATEFORMAT
        )
        app_handler = logging.handlers.RotatingFileHandler(
            filename=os.path.join(LOG_FILE_PATH, LOG_FILE_NAME),
            maxBytes=constants.ROTATION_CONDITION,
            backupCount=constants.RETENTION_TIME,
        )
        app_handler.setFormatter(log_formatter)
        app_handler.setLevel(log_level.get(LOG_LEVEL, logging.INFO))

        self.logger.addHandler(app_handler)
        self.logger.setLevel(log_level.get(LOG_LEVEL, logging.INFO))

    def get(self):
        """
        Method to return the instance logger
        """
        return self.logger


def get_logger() -> logging.Logger:
    """
    Gets the logger to log debug and informational messages.
    """
    log = Logger()
    return log.get()
