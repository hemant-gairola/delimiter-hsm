#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

from typing import Union

from fastapi import APIRouter, Path
from pydantic import conint
from src.validators.unload_validator import (ExecutionStatus, SourceData,
                                             Unload, UnloadResponse)

router = APIRouter(
    prefix="/unload",
    tags=["UnloadProcess"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "",
    response_model=None,
    summary="Create a unload process to unload data to files from the source database.",  # noqa
    responses={"201": {"model": UnloadResponse}},
)
def create_unload(body: Unload) -> Union[None, UnloadResponse]:
    """
    Create a unload process to unload data to files from the source database.
    """
    pass


@router.get(
    "/status/{executionId}",
    response_model=UnloadResponse,
    summary="Returns a Unload status by execution ID.",
)
def get_unload_status_by_execution_id(
    execution_id: conint(ge=1) = Path(..., alias="executionId")
) -> UnloadResponse:
    """
    Returns a Unload status by execution ID.
    """
    pass


@router.put(
    "/status/{executionId}",
    response_model=None,
    summary="Update status of existing execution.",
)
def update_execution_status(
    execution_id: conint(ge=1) = Path(..., alias="executionId"),
    body: ExecutionStatus = ...,
) -> None:
    """
    Update status of existing execution.
    """
    pass


@router.delete(
    "/executions/{executionId}",
    response_model=None,
    summary="Cleanup the existing unload execution.",
)
def clean_up_execution(
    execution_id: conint(ge=1) = Path(..., alias="executionId")
) -> None:
    """
    Cleanup the existing unload execution.
    """
    pass


@router.get(
    "/source-data/{executionId}",
    response_model=SourceData,
    summary="Returns the source data by execution ID.",
)
def get_source_data_by_execution_id(
    execution_id: conint(ge=1) = Path(..., alias="executionId")
) -> SourceData:
    """
    Returns the source data by execution ID.
    """
    pass
