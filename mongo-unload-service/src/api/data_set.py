#
# Copyright (c) 2023 by Delphix. All rights reserved.
#


from typing import List, Union

from fastapi import APIRouter
from pydantic import conint
from src.validators.data_set_validator import DataSet

router = APIRouter()


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
