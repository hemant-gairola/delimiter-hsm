#
# Copyright (c) 2023 by Delphix. All rights reserved.
#
import hashlib
import json
import os
from typing import List, Union

import requests
from fastapi import APIRouter, Depends, Path
from pydantic import conint
from sqlalchemy.orm import Session
from src.business_logic import unload_split as us
from src.databases.database import SessionLocal, engine
from src.models.source_data import Base as source_base
from src.models.source_data_info import Base as source_data_info_base
from src.models.unload_process import Base as unload_base
from src.models.unload_process_data_info import \
    Base as unload_process_data_info_base
from src.repository.base_repository import BaseRepository
from src.validators.unload_validator import (ExecutionStatus, SourceData,
                                             Unload, UnloadResponse)

router = APIRouter()

base_repo = BaseRepository()

unload_base.metadata.create_all(bind=engine)
source_base.metadata.create_all(bind=engine)

source_data_info_base.metadata.create_all(bind=engine)
unload_process_data_info_base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    tags=["UnloadProcess"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/unload",
    response_model=None,
    summary="Create a unload process to unload data to files from the source database.",  # noqa
    responses={"201": {"model": UnloadResponse}},
)
def create_unload(
    body: Unload, db: Session = Depends(get_db)
) -> Union[None, UnloadResponse]:
    """
    Create a unload process to unload data to files from the source database.
    """
    unload_path = "/etc/hyperscale"
    # unload_path = "/Users/hemant.gairola/all_code/hemant_hsc_github/delimiter-hsm/mongo-unload-service"
    # os.makedirs(name=unload_path, exist_ok=True)
    # Get mount_name from mask-service/mount-filesystems/{mountFileSystemId}
    # api = "http://hs-engine3.dlpxdc.co:8080/api/mount-filesystems/1"
    # # api="http://mask-service:8080/api/mount-filesystems/1"
    # get_mask_data_mount_data=get_data(api=api)
    # mount_name = get_mask_data_mount_data['mountName']
    mount_name = "abc3"
    os.makedirs(name=f"{unload_path}/{mount_name}", exist_ok=True)

    # We'll add data into
    # 1.source_data_info,
    # 2. source_data,
    # 3. unload_process
    # 4. unload_process_data_info,
    # Status : PROCESS -> SUCCEED/FAILED
    # Step 1: Read the file and capture the fmt data
    # Step 2: Split the files as per the give spit count
    # Step 3: Prepare for each split file
    # {"executionId":5,"sourceKey":{"schema_name":"DLPXDBORA","table_name":"HTAB2"},"unloadFilePath":"/etc/hyperscale/abc3/1/src/8767199970ae27ffbe4de378f73378fd/7d63dc84e3013b6faa267fc50c3fe686/7d63dc84e3013b6faa267fc50c3fe686_0.csv","rowsUnloaded":0,"status":"CREATED","error":null}
    # Step 4: With step 3, prepare table unload_process: {"executionId":5,"jobId":1,"datasetId":6,"sourceConfigs":{"max_concurrent_source_connection":30},"status":"SUCCEEDED","startTime":"2023-06-19T15:40:59.568867","endTime":"2023-06-19T15:41:29.802821","error":null,"dataInfo":null}
    # Keep updating the table unload_process
    # In parallel to stpe 2, make entry in source_data_info : {"executionId":5,"sourceKey":{"schema_name":"DLPXDBORA","table_name":"HTAB2"},"unloadSplitCount":4,"totalNumberOfRows":0,"maskingSplitCount":null}
    id_dict = body.dict()
    execution_id = id_dict["execution_id"]
    job_id = id_dict["job_id"]
    dataset_id = id_dict["dataset_id"]

    data_set_info = base_repo.getById(id=dataset_id, db=db)
    parsed_data = json.loads(data_set_info.data)
    parsed_data_info = parsed_data["data_info"][0]
    source_file = parsed_data_info["source_files"][0]
    unload_split = parsed_data_info["unload_split"]
    schema_name = parsed_data_info["schema_name"]
    table_name = parsed_data_info["table_name"]
    format_file_name = parsed_data_info["format_file"]

    print(f"Hemant 11 : {parsed_data['data_info']}")
    cwd = os.getcwd()
    input_file = os.path.join(cwd, source_file)
    output_target = os.path.join(cwd, "output")
    format_file_name_full_path = os.path.join(cwd, format_file_name)
    with open(format_file_name_full_path) as f:
        lines = f.readlines()
    print(f"Hemant 22 : {lines}")
    format_dict = dict(item.split(":") for item in lines)
    column_names = list(format_dict.keys())
    # Create target folder structure
    target_file_path = (
        f"/etc/hyperscale/{mount_name}/{job_id}/src/{schema_name}/{table_name}/"
    )
    # Local target path
    # target_file_path = "/Users/hemant.gairola/all_code/hemant_hsc_github/delimiter-hsm/mongo-unload-service/output"
    os.makedirs(name=f"{target_file_path}", exist_ok=True)

    # Prepare source key
    source_key = {"schema_name": schema_name, "table_name": table_name}
    unload_data = body.dict()
    unload_split_count = 4
    table_row_count_map = 250

    print(f"FOr Hemant 00 : {unload_data}")

    # Make entry in source_data_info
    save_into_source_data_response = base_repo.save_into_source_data(
        source_key, unload_data, unload_split_count, table_row_count_map, db
    )
    print(f"For Hemant : {save_into_source_data_response}")
    # Splitting taking place here
    us.split_arrow_without_slice(
        input_file=input_file,
        delimiter=",",
        column_names=column_names,
        output_file_dir=target_file_path,
        split_row_count=250,
    )

    # Make entry in unload_process_data_info
    all_splitted_files = os.listdir(target_file_path)
    for files in all_splitted_files:
        file_full_path = os.path.join(target_file_path, files)
        base_repo.save_into_unload_process_data_info(
            source_key, execution_id, file_full_path, db
        )

    # pass


@router.get(
    "/unload/status/{executionId}",
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
    "/unload/status/{executionId}",
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
def get_source_data_by_execution_id(execution_id: int, db: Session = Depends(get_db)) -> SourceData:
    """
    Returns the source data by execution ID.
    """
    data = base_repo.getByIdsourceData(id=execution_id, db=db)
    parsed_data = json.loads(data.data)
    response = {
        "status":"SUCCEEDED",
        "sourceInfo":[]
    }
    return SourceData(**response)


########################################
# Some extra dunctions
def get_data(api, parameter=""):
    response = requests.get(f"{api}")
    if response.status_code == 200:
        print("sucessfully fetched the data")
        print(response.json()["mountName"])
    else:
        print(f"Hello person, there's a {response.status_code} error with your request")
    return response.json()
