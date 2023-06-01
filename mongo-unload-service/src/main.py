#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.api.api_version import router as api_version_router
from src.api.connector_management import router as connector_router

app = FastAPI(
    title="MongoDB Delphix Hyperscale Unload Service",
    version="v1.0.0",
    description="Delphix Hyperscale Unload Service API",
    contact={
        "name": "Delphix Support",
        "url": "https://support.delphix.com",
        "email": "support@delphix.com",
    },
    # servers=[{'url': '/api'}],
)


# register the routers for APIs
app.include_router(api_version_router, prefix="/api")
app.include_router(connector_router, prefix="/api")


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")
