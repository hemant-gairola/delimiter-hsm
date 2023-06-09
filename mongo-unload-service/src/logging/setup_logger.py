import logging
import logging.handlers
import os
import threading
from src.utils import constants


LOG_FILE_NAME = "sdm.log"
MONITOR_LOG_FILE_NAME = "monitor.log"
LOG_LEVEL = os.getenv("SDM_LOG_LEVEL", "INFO")
ROTATION_CONDITION = 5242880
RETENTION_TIME = 100
TRACE = 8

_lock = threading.Lock()

log_level = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "TRACE": TRACE,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}


class SalesforceLogger(logging.Logger):
    def __init__(self, level=logging.NOTSET):
        super().__init__(name="Salesforce", level=level)

    def trace(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'TRACE'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.trace("Houston, we have a %s", "bit of a problem", exc_info=1)
        """
        if self.isEnabledFor(TRACE):
            self._log(TRACE, msg, args, **kwargs)


class Singleton(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        global _lock
        with _lock:
            if cls not in cls.__instances:
                cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


class MonitorFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Determine if the specified record is to be logged.

        Returns True if the record should be logged, or False otherwise.
        If deemed appropriate, the record may be modified in-place.
        """
        return record.module == "monitor"


class SDMFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Determine if the specified record is to be logged.

        Returns True if the record should be logged, or False otherwise.
        If deemed appropriate, the record may be modified in-place.
        """
        return record.module != "monitor"


class SalesforceFileHandler(logging.FileHandler):
    def __init__(
        self, filename, mode="a", encoding=None, delay=False, errors=None
    ):
        directory = os.path.dirname(filename)
        os.makedirs(directory, exist_ok=True)
        super().__init__(filename, mode, encoding, delay, errors)


class Logger(metaclass=Singleton):
    def __init__(self):
        logging_format = (
            "[%(asctime)s] [%(levelname)s]"
            " [%(filename)s:%(lineno)d] %(message)s"
        )
        logging.addLevelName(TRACE, "TRACE")
        self.logger = SalesforceLogger()
        log_formatter = logging.Formatter(
            logging_format, datefmt="%Y-%m-%dT%H:%M:%S %Z"
        )
        sdm_handler = SalesforceFileHandler(
            filename=os.path.join(constants.LOG_FILE_LOCATION, LOG_FILE_NAME)
        )
        sdm_handler.setFormatter(log_formatter)
        sdm_handler.setLevel(log_level.get(LOG_LEVEL, logging.INFO))
        sdm_handler.addFilter(SDMFilter())

        monitor_handler = logging.handlers.RotatingFileHandler(
            filename=os.path.join(
                constants.LOG_FILE_LOCATION, MONITOR_LOG_FILE_NAME
            ),
            maxBytes=ROTATION_CONDITION,
            backupCount=RETENTION_TIME,
        )
        monitor_handler.setFormatter(log_formatter)
        monitor_handler.setLevel(log_level.get(LOG_LEVEL, logging.INFO))
        monitor_handler.addFilter(MonitorFilter())

        self.logger.addHandler(sdm_handler)
        self.logger.addHandler(monitor_handler)
        self.logger.setLevel(log_level.get(LOG_LEVEL, logging.INFO))

    def get(self):
        return self.logger


def get_logger() -> logging.Logger:
    """
    Gets the logger to log debug and informational messages.
    """
    log = Logger()
    return log.get()
