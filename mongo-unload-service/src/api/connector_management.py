#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

import json
from typing import List, Union

from fastapi import APIRouter, Depends, Path
from pydantic import conint
from sqlalchemy.orm import Session
from src.databases.database import SessionLocal, engine
from src.models.connector import Base as base_connector
from src.repository.base_repository import BaseRepository
from src.validators.connector_validator import Connector, ConnectorResponse

router = APIRouter()

base_repo = BaseRepository()

base_connector.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
def create_connector(
    body: Connector, db: Session = Depends(get_db)
) -> Union[None, ConnectorResponse]:
    """
    Create Connector.
    """

    data = base_repo.save_data_into_connector(body.dict(), db=db)
    parsed_data = json.loads(data.data)
    response = {
        "id": data.id,
        "jdbc_url": parsed_data["jdbcUrl"],
        "user": parsed_data["user"],
    }
    return ConnectorResponse(**response)


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
