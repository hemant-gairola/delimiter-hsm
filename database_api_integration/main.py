
from uvicorn import run as runserver
from fastapi import FastAPI

from todo.models import create_tables
from todo.controllers import router

app = FastAPI(title="TODO APP",
              description="FastAPI Application POC with Swagger and Sqlalchemy",
              version="1.0.0", )


# @app.exception_handler(Exception)
# def validation_exception_handler(request, err):
#     base_error_message = f"Failed to execute: {request.method}: {request.url}"
#     return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


# @app.middleware("http")
# async def add_process_time_header(request, call_next):
#     print('inside middleware!')
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
#     return response



# Include router(s)
app.include_router(router, prefix="/v1")

@app.on_event("startup")
async def startup():
    """
    This function creates the database tables when the server starts.
    """
    await create_tables()

@app.get("/")
async def root() -> dict:
    """
    Root api view.

    :return: dictionary with a message key
    """
    return {"message": "PoC for Fastapi and sqlalchemy integration"}


if __name__ == "__main__":
    runserver("main:app", host="0.0.0.0", port=8080, reload=True)
