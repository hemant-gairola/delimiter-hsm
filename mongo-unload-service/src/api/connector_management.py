#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

from typing import List, Union

from fastapi import APIRouter, Path
from pydantic import conint
from src.validators.connector_validator import Connector, ConnectorResponse

router = APIRouter(
    prefix="/connectors",
    tags=["ConnectorManagement"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "",
    response_model=None,
    responses={"201": {"model": ConnectorResponse}},
)
def create_connector(body: Connector) -> Union[None, ConnectorResponse]:
    """
    Create Connector.
    """
    pass


@router.get(
    "",
    response_model=List[ConnectorResponse],
)
def list_all_connector() -> List[ConnectorResponse]:
    """
    Returns a list of connectors.
    """
    pass


@router.get(
    "/{connector_id}",
    response_model=ConnectorResponse,
)
def get_connector(
    connector_id: conint(ge=1) = Path(..., alias="connectorId")
) -> ConnectorResponse:
    """
    Get connector by Id.
    """
    pass


@router.put(
    "/{connector_id}",
    response_model=ConnectorResponse,
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
    "/{connector_id}",
    response_model=None,
)
def delete_connector(
    connector_id: conint(ge=1) = Path(..., alias="connectorId")
) -> None:
    """
    Remove a Connector.
    """
    pass
