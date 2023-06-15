import configparser
from functools import lru_cache
from src.utils import constants


@lru_cache
def get_config() -> configparser.ConfigParser:
    """
    Responsible for reading the default config file

    Returns:
        ConfigParser object which can be called as a dictionary
    """
    parser = configparser.ConfigParser()
    parser.read(constants.CONFIG_FILE_PATH)
    return parser


config = get_config()
log_file = config["logging"]["log_file"]
log_level = config["logging"]["log_level"]

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": constants.FORMATTER,
            "datefmt": constants.DATEFORMAT,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "rotating-file-handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": log_file,
            "maxBytes": constants.ROTATION_CONDITION,
            "backupCount": constants.BACKUP_COUNT,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "app-logger": {
            "handlers": ["default", "rotating-file-handler"],
            "level": log_level,
        },
    },
}
