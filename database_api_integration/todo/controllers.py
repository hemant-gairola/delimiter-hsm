# FastAPI Imports
from fastapi import APIRouter
from starlette import status

# Own Imports
from todo.schemas import CreateTaskSchema, GetTaskSchema, ListTasksSchema
from todo import services


# Initialize api router
router = APIRouter()

@router.post('/task', tags=["TASKS"], status_code=status.HTTP_201_CREATED)
async def create_task(payload: CreateTaskSchema):
    created_task = await services.create_task(payload = payload)
    return created_task

@router.get('/tasks', tags=["TASKS"], response_model=ListTasksSchema, status_code=status.HTTP_200_OK)
def get_all_tasks():
    tasks_list = services.get_all_tasks()
    return tasks_list