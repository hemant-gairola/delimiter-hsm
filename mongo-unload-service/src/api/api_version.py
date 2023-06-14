#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

import logging

from fastapi import APIRouter
from src.config import get_config
from src.validators.api_version import ApiVersion

config = get_config()
logger = logging.getLogger("app-logger")

router = APIRouter(
    prefix="/api-version",
    tags=["ApiVersion"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "", response_model=ApiVersion, summary="Returns the API version of service"
)  # noqa
def get_api_version() -> ApiVersion:
    """
    Returns the API version of service
    """
    logger.info("get api version called")
    return ApiVersion(versionId=config["default"]["version"])
