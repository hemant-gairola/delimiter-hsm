#
# Copyright (c) 2023 by Delphix. All rights reserved.
#


import json
from typing import List, Union

from fastapi import APIRouter, Depends
from pydantic import conint
from sqlalchemy.orm import Session
from src.databases.database import SessionLocal, engine
from src.models.data_set import Base
from src.repository.base_repository import BaseRepository
from src.validators.data_set_validator import DataSet, DataSetResponse

router = APIRouter()

base_repo = BaseRepository()

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/data-sets",
    response_model=None,
    summary="Create a Data Set.",
    responses={"201": {"model": DataSet}},
    tags=["DataSets"],
    status_code=201,
)
# def create_data_set(body: dict, db:Session = Depends(get_db)) -> Union[None, DataSet]:
def create_data_set(
    body: DataSet, db: Session = Depends(get_db)
) -> Union[None, DataSet]:
    """
    Create a Data Set.
    """

    data = base_repo.save(body.dict(), db=db)
    parsed_data = json.loads(data.data)
    response = {
        "id": data.id,
        "connector_id": parsed_data["connector_id"],
        "mount_filesystem_id": parsed_data["mount_filesystem_id"],
        "data_info": parsed_data["data_info"],
    }
    return DataSet(**response)


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
def get_data_set_by_id(id: int, db: Session = Depends(get_db)) -> DataSet:
    """
    Returns a Data Set by ID.
    """
    data = base_repo.getById(id=id, db=db)
    parsed_data = json.loads(data.data)
    response = {
        "id": data.id,
        "connector_id": parsed_data["connector_id"],
        "mount_filesystem_id": parsed_data["mount_filesystem_id"],
        "data_info": parsed_data["data_info"],
    }
    return DataSet(**response)


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
