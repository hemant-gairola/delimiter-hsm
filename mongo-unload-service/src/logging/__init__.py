#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

import logging
from src.utils import constants
from src.config import get_config

config = get_config()

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
        # "file-handler": {
        #     "formatter": "default",
        #     "class": "handlers.RotatingFileHandler",
        #     "args": (config['logging']['log_file'], 'a', constants.ROTATION_CONDITION, constants.RETENTION_TIME), # noqa
        # },
    },
    "loggers": {
        "app-logger": {
            "handlers": ["default"],
            "level": logging.getLogger("gunicorn.error").level,
        },
    },
}
