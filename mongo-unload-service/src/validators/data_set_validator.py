#
# Copyright (c) 2023 by Delphix. All rights reserved.
#
from typing import List, Optional

from pydantic import BaseModel, Field, constr


class DataInfoItem(BaseModel):
    schema_name: constr(min_length=1) = Field(
        ..., description="Database Schema name of source data."
    )
    table_name: constr(min_length=1) = Field(
        ..., description="Database Table name of source data."
    )
    filter_key: Optional[constr(min_length=1)] = Field(
        None,
        description="The unique database column field to filter the source data.",  # noqa
    )
    unload_split: Optional[int] = Field(
        1,
        description="The number of unloaded files to be generated from the source database.",  # noqa
    )


class DataSet(BaseModel):
    id: Optional[int] = None
    connector_id: int = Field(
        ...,
        description="ID of the Connector model to be used for this Data Set.",  # noqa
    )
    mount_filesystem_id: int = Field(
        ...,
        description="ID of the Mount Filesystem model to be used for this Data Set.",  # noqa
    )
    data_info: List[DataInfoItem] = Field(
        ...,
        description="Array of multiple objects, each providing the information of the table, schema etc.",  # noqa
        max_items=10000,
        min_items=1,
    )
