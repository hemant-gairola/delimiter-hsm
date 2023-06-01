#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

from fastapi import APIRouter
from src.validators.api_version import ApiVersion

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
    return ApiVersion(versionId="1.0.0")
