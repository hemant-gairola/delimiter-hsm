#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.api.api_version import router as api_version_router
from src.api.connector_management import router as connector_router
from src.api.unload import router as unload_router

app = FastAPI()

sub_app = FastAPI(
    title="MongoDB Delphix Hyperscale Unload Service",
    version="v1.0.0",
    description="Delphix Hyperscale Unload Service API",
    contact={
        "name": "Delphix Support",
        "url": "https://support.delphix.com",
        "email": "support@delphix.com",
    },
)

# register the routers for APIs
sub_app.include_router(api_version_router)
sub_app.include_router(connector_router)
sub_app.include_router(unload_router)

app.mount("/api", sub_app)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/api/docs")
