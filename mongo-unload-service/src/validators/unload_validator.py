#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, constr


class SourceConfigs(BaseModel):
    """
    Pydantic Model for SourceConfigs
    """

    max_concurrent_source_connection: Optional[int] = Field(
        None,
        description="Maximum number of parallel connection that hyperscale can have with source datasource.",  # noqa
    )


class Status(str, Enum):
    """The status of the Unload process."""

    CREATED = "CREATED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"


class DataInfoItem1(BaseModel):
    """
    Pydantic Model for DataInfoItem1
    """

    source_key: Dict[str, str] = Field(
        ...,
        description="object providing the information like schema_name, table_name or file_name of the source datasource",  # noqa
    )
    rows_unloaded: int = Field(
        ...,
        description="Total number of rows unloaded from the database table.",  # noqa
    )
    unload_file_path: constr(min_length=1) = Field(
        ..., description="relative path of the unload source file."
    )
    status: Status = Field(..., description="The status of the unload process.")  # noqa
    error: Optional[str] = Field(None, description="Exception details.")


class ExecutionStatus(BaseModel):
    """
    Pydantic Model for ExecutionStatus
    """

    status: Status = Field(..., description="The status of the Unload process.")  # noqa
    error: Optional[str] = Field(None, description="Optional, error detail.")


class Unload(BaseModel):
    """
    Pydantic Model for Unload
    """

    execution_id: int = Field(..., description="The Unload object entity ID.")
    job_id: int = Field(
        ..., description="ID of the Job model to be used for this Unload."
    )
    dataset_id: int = Field(
        ..., description="ID of the Data Set model to be used for this Unload."
    )
    source_configs: Optional[SourceConfigs] = Field(
        None, description="configuration properties for source datasource"
    )


class SourceInfoItem(BaseModel):
    """
    Pydantic Model for SourceInfoItem
    """

    source_key: Dict[str, str] = Field(
        ...,
        description="Object providing the information like schema_name, table_name or file_name of the source datasource",  # noqa
    )
    unload_split_count: int = Field(
        ...,
        description="The number of unloaded files to be generated from the source database.",  # noqa
    )
    total_number_of_rows: int = Field(
        ...,
        description="Total number of rows unloaded from the database table.",  # noqa
    )
    masking_split_count: Optional[int] = Field(
        None, description="The number of masked splitted files to be generated."  # noqa
    )


class SourceData(BaseModel):
    """
    Pydantic Model for SourceData
    """

    status: Optional[Status] = Field(
        None, description="The status of the Unload process."
    )
    source_info: Optional[List[SourceInfoItem]] = Field(
        None,
        description="Array of multiple objects, each object providing the information like sourceKey, unloadSplitCount etc.",  # noqa
        max_items=10000,
        min_items=1,
    )


class UnloadResponse(ExecutionStatus):
    """
    Pydantic Response Model for UnloadResponse
    """

    execution_id: int = Field(..., description="The Unload object entity ID.")
    job_id: int = Field(
        ..., description="ID of the Job model to be used for this Unload."
    )
    start_time: str = Field(
        ..., description="The time when the unload process is started."
    )
    end_time: Optional[str] = Field(
        None, description="The time when the unload process is completed."
    )
    data_info: List[DataInfoItem1] = Field(
        ...,
        description="Array of multiple objects, each object providing the information like sourceKey and file_info.",  # noqa
        max_items=10000,
        min_items=1,
    )
