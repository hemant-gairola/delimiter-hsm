#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

import logging
from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.responses import RedirectResponse
from src.api.api_version import router as api_version_router
from src.api.connector_management import router as connector_router
from src.api.data_set import router as data_set_router
from src.api.unload import router as unload_router
from src.config import get_config
from src.logging import log_config

# handle the gunicorn log handler
gunicorn_logger = logging.getLogger("gunicorn.error")
logger.handlers = gunicorn_logger.handlers

if __name__ != "main":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)

# load the log config before initializing FastAPI
dictConfig(log_config)

config = get_config()
app = FastAPI()

sub_app = FastAPI(
    title="MongoDB Delphix Hyperscale Unload Service",
    version=config["default"]["version"],
    description="Delphix Hyperscale Unload Service API",
    contact={
        "name": "Delphix Support",
        "url": "https://support.delphix.com",
        "email": "support@delphix.com",
    },
)

# register the routers for APIs
sub_app.include_router(api_version_router)
sub_app.include_router(connector_router)
sub_app.include_router(unload_router)
sub_app.include_router(data_set_router)

app.mount("/api", sub_app)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    """
    Redirects the page to /api/docs
    """
    return RedirectResponse(url="/api/docs")


# #### For Debugging on Local #####
# if __name__ == "__main__":
#     from uvicorn import run as runserver
#     runserver("src.main:app", host="0.0.0.0", port=8080)
