#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

# generated by fastapi-codegen:
#   filename:  api.yaml
#   timestamp: 2023-06-01T05:37:27+00:00

from __future__ import annotations

from typing import List, Union

import uvicorn
from fastapi import APIRouter, FastAPI, Path
from models import (
    ApiVersion,
    Connector,
    ConnectorResponse,
    DataSet,
    ExecutionStatus,
    SourceData,
    Unload,
    UnloadResponse,
)
from pydantic import conint

app = FastAPI(
    title="Delphix Hyperscale Unload Service",
    version="v1.0.0",
    description="Delphix Hyperscale Unload Service API",
    contact={
        "name": "Delphix Support",
        "url": "https://support.delphix.com",
        "email": "support@delphix.com",
    },
    servers=[{"url": "/api"}],
    # openapi_prefix="/api",
    # root_path="/api",
    # root_path_in_servers=False,
)

router = APIRouter()


@router.get(
    "/api-version",
    response_model=ApiVersion,
    summary="Returns the API version of service",
    tags=["ApiVersion"],
)
def get_api_version() -> ApiVersion:
    """
    Returns the API version of service
    """
    print("aaya")
    return ApiVersion(versionId="1.2.0")


@router.post(
    "/connectors",
    response_model=None,
    summary="Create Connector.",
    responses={"201": {"model": ConnectorResponse}},
    tags=["ConnectorManagement"],
)
def create_connector(body: Connector) -> Union[None, ConnectorResponse]:
    """
    Create Connector.
    """
    pass


@router.get(
    "/connectors",
    response_model=List[ConnectorResponse],
    summary="Returns a list of connectors.",
    tags=["ConnectorManagement"],
)
def list_all_connector() -> List[ConnectorResponse]:
    """
    Returns a list of connectors.
    """
    pass


@router.get(
    "/connectors/{connector_id}",
    response_model=ConnectorResponse,
    summary="Get connector by Id.",
    tags=["ConnectorManagement"],
)
def get_connector(
    connector_id: conint(ge=1) = Path(..., alias="connectorId")
) -> ConnectorResponse:
    """
    Get connector by Id.
    """
    pass


@router.put(
    "/connectors/{connector_id}",
    response_model=ConnectorResponse,
    summary="Update a Connector.",
    tags=["ConnectorManagement"],
)
def update_connector(
    connector_id: conint(ge=1) = Path(..., alias="connectorId"),
    body: Connector = ...,  # noqa
) -> ConnectorResponse:
    """
    Update a Connector.
    """
    pass


@router.delete(
    "/connectors/{connector_id}",
    response_model=None,
    summary="Remove a Connector.",
    tags=["ConnectorManagement"],
)
def delete_connector(
    connector_id: conint(ge=1) = Path(..., alias="connectorId")
) -> None:
    """
    Remove a Connector.
    """
    pass


@router.post(
    "/data-sets",
    response_model=None,
    summary="Create a Data Set.",
    responses={"201": {"model": DataSet}},
    tags=["DataSets"],
)
def create_data_set(body: DataSet) -> Union[None, DataSet]:
    """
    Create a Data Set.
    """
    pass


@router.get(
    "/data-sets",
    response_model=List[DataSet],
    summary="Returns a list of Data Sets.",
    tags=["DataSets"],
)
def list_all_data_set() -> List[DataSet]:
    """
    Returns a list of Data Sets.
    """
    pass


@router.get(
    "/data-sets/{id}",
    response_model=DataSet,
    summary="Returns a Data Set by ID.",
    tags=["DataSets"],
)
def get_data_set_by_id(id: conint(ge=1)) -> DataSet:
    """
    Returns a Data Set by ID.
    """
    pass


@router.put(
    "/data-sets/{id}",
    response_model=DataSet,
    summary="Update an existing Data Set.",
    tags=["DataSets"],
)
def update_data_set(id: conint(ge=1), body: DataSet = ...) -> DataSet:
    """
    Update an existing Data Set.
    """
    pass


@router.delete(
    "/data-sets/{id}",
    response_model=None,
    summary="Delete an existing Data Set.",
    tags=["DataSets"],
)
def delete_data_set(id: conint(ge=1)) -> None:
    """
    Delete an existing Data Set.
    """
    pass


@router.delete(
    "/executions/{execution_id}",
    response_model=None,
    summary="Cleanup the existing unload execution.",
    tags=["UnloadProcess"],
)
def clean_up_execution(
    execution_id: conint(ge=1) = Path(..., alias="executionId")
) -> None:
    """
    Cleanup the existing unload execution.
    """
    pass


@router.get(
    "/source-data/{execution_id}",
    response_model=SourceData,
    summary="Returns the source data by execution ID.",
    tags=["UnloadProcess"],
)
def get_source_data_by_execution_id(
    execution_id: conint(ge=1) = Path(..., alias="executionId")
) -> SourceData:
    """
    Returns the source data by execution ID.
    """
    pass


@router.post(
    "/unload",
    response_model=None,
    summary="Create a unload process to unload data to files from the source database.",  # noqa
    responses={"201": {"model": UnloadResponse}},
    tags=["UnloadProcess"],
)
def create_unload(body: Unload) -> Union[None, UnloadResponse]:
    """
    Create a unload process to unload data to files from the source database.
    """
    pass


@router.get(
    "/unload/status/{execution_id}",
    response_model=UnloadResponse,
    summary="Returns a Unload status by execution ID.",
    tags=["UnloadProcess"],
)
def get_unload_status_by_execution_id(
    execution_id: conint(ge=1) = Path(..., alias="executionId")
) -> UnloadResponse:
    """
    Returns a Unload status by execution ID.
    """
    pass


@router.put(
    "/unload/status/{execution_id}",
    response_model=None,
    summary="Update status of existing execution.",
    tags=["UnloadProcess"],
)
def update_execution_status(
    execution_id: conint(ge=1) = Path(..., alias="executionId"),
    body: ExecutionStatus = ...,
) -> None:
    """
    Update status of existing execution.
    """
    pass


app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", port=9090, log_level="debug", reload=True)
