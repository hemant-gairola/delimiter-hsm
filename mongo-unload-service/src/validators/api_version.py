#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

from pydantic import BaseModel, Field, constr


class ApiVersion(BaseModel):
    versionId: constr(min_length=1, max_length=50) = Field(
        ...,
        description="The VersionId is used to return the current version of service.",  # noqa
    )
