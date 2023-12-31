#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

# generated by fastapi-codegen:
#   filename:  api.yaml
#   timestamp: 2023-06-01T05:29:27+00:00

from __future__ import annotations

from typing import List, Union

from fastapi import FastAPI, Path
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
    version="v3.1.0",
    description="Delphix Hyperscale Unload Service API",
    contact={
        "name": "Delphix Support",
        "url": "https://support.delphix.com",
        "email": "support@delphix.com",
    },
    servers=[{"url": "/api"}],
)


@app.get("/api-version", response_model=ApiVersion, tags=["ApiVersion"])
def get_api_version() -> ApiVersion:
    """
    Returns the API version of service
    """
    pass


@app.post(
    "/connectors",
    response_model=None,
    responses={"201": {"model": ConnectorResponse}},
    tags=["ConnectorManagement"],
)
def create_connector(body: Connector) -> Union[None, ConnectorResponse]:
    """
    Create Connector.
    """
    pass


@app.get(
    "/connectors",
    response_model=List[ConnectorResponse],
    tags=["ConnectorManagement"],  # noqa
)
def list_all_connector() -> List[ConnectorResponse]:
    """
    Returns a list of connectors.
    """
    pass


@app.get(
    "/connectors/{connector_id}",
    response_model=ConnectorResponse,
    tags=["ConnectorManagement"],
)
def get_connector(
    connector_id: conint(ge=1) = Path(..., alias="connectorId")
) -> ConnectorResponse:
    """
    Get connector by Id.
    """
    pass


@app.put(
    "/connectors/{connector_id}",
    response_model=ConnectorResponse,
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


@app.delete(
    "/connectors/{connector_id}",
    response_model=None,
    tags=["ConnectorManagement"],  # noqa
)
def delete_connector(
    connector_id: conint(ge=1) = Path(..., alias="connectorId")
) -> None:
    """
    Remove a Connector.
    """
    pass


@app.post(
    "/data-sets",
    response_model=None,
    responses={"201": {"model": DataSet}},
    tags=["DataSets"],
)
def create_data_set(body: DataSet) -> Union[None, DataSet]:
    """
    Create a Data Set.
    """
    pass


@app.get("/data-sets", response_model=List[DataSet], tags=["DataSets"])
def list_all_data_set() -> List[DataSet]:
    """
    Returns a list of Data Sets.
    """
    pass


@app.get("/data-sets/{id}", response_model=DataSet, tags=["DataSets"])
def get_data_set_by_id(id: conint(ge=1)) -> DataSet:
    """
    Returns a Data Set by ID.
    """
    pass


@app.put("/data-sets/{id}", response_model=DataSet, tags=["DataSets"])
def update_data_set(id: conint(ge=1), body: DataSet = ...) -> DataSet:
    """
    Update an existing Data Set.
    """
    pass


@app.delete("/data-sets/{id}", response_model=None, tags=["DataSets"])
def delete_data_set(id: conint(ge=1)) -> None:
    """
    Delete an existing Data Set.
    """
    pass


@app.delete(
    "/executions/{execution_id}", response_model=None, tags=["UnloadProcess"]
)  # noqa
def clean_up_execution(
    execution_id: conint(ge=1) = Path(..., alias="executionId")
) -> None:
    """
    Cleanup the existing unload execution.
    """
    pass


@app.get(
    "/source-data/{execution_id}",
    response_model=SourceData,
    tags=["UnloadProcess"],  # noqa
)
def get_source_data_by_execution_id(
    execution_id: conint(ge=1) = Path(..., alias="executionId")
) -> SourceData:
    """
    Returns the source data by execution ID.
    """
    pass


@app.post(
    "/unload",
    response_model=None,
    responses={"201": {"model": UnloadResponse}},
    tags=["UnloadProcess"],
)
def create_unload(body: Unload) -> Union[None, UnloadResponse]:
    """
    Create a unload process to unload data to files from the source database.
    """
    pass


@app.get(
    "/unload/status/{execution_id}",
    response_model=UnloadResponse,
    tags=["UnloadProcess"],
)
def get_unload_status_by_execution_id(
    execution_id: conint(ge=1) = Path(..., alias="executionId")
) -> UnloadResponse:
    """
    Returns a Unload status by execution ID.
    """
    pass


@app.put(
    "/unload/status/{execution_id}", response_model=None, tags=["UnloadProcess"]  # noqa
)  # noqa
def update_execution_status(
    execution_id: conint(ge=1) = Path(..., alias="executionId"),
    body: ExecutionStatus = ...,
) -> None:
    """
    Update status of existing execution.
    """
    pass
