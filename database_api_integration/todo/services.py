from todo.repositories import task_repository
from todo import schemas


async def create_task(payload: schemas.CreateTaskSchema):
    created_task =  await task_repository.create(payload=payload)
    return created_task

def get_all_tasks() -> schemas.ListTasksSchema:
    tasks_list = task_repository.fetch_all()

    return schemas.ListTasksSchema(tasks=tasks_list)