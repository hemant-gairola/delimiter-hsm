#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

from typing import Dict, Optional

from pydantic import BaseModel, Field, constr


class ConnectorResponse(BaseModel):
    id: Optional[int] = Field(
        None, description="The Connector object entity ID."
    )  # noqa
    user: constr(min_length=1, max_length=256) = Field(
        ..., description="The username of this connector."
    )
    jdbc_url: constr(min_length=1, max_length=256) = Field(
        ..., description="The jdbc url of this connector."
    )
    # connection_properties: Optional[Dict[str, str]] = Field(
    #     None, description="The properties of this connector."
    # )


class Connector(ConnectorResponse):
    password: constr(min_length=1, max_length=256) = Field(
        ..., description="The password of this connector."
    )
    restoreSensitiveFields: Optional[bool] = Field(
        False,
        description="Passed to indicate that user want to restore the sensitive data.",  # noqa
    )
    jdbc_url: constr(min_length=1, max_length=256) = Field(
        ..., description="The jdbc url of this connector."
    )
    user: constr(min_length=1, max_length=256) = Field(
        ..., description="The username of this connector."
    )
