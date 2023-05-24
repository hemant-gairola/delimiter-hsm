
import datetime
import uuid

from sqlalchemy.orm import Session

from . import models, schemas
from configuration.deps import get_db

class TaskRepository:

    def __init__(self) -> None:
        self.db: Session = get_db().__next__()

    async def create(self, payload: schemas.CreateTaskSchema):
        db_item = models.Task(
            created=datetime.datetime.utcnow(),
            updated=datetime.datetime.utcnow(),
            priority=payload.priority.value,
            status=payload.status.value,
            task=payload.task,
            user_id=uuid.uuid4().hex
        )
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)

        task = db_item.dict()
        return task

    def fetch_by_id(self, _id: str):
        return self.db.query(models.Task).filter(models.Task.id == _id).first()

    def fetch_by_name(self, name: str):
        return self.db.query(models.Task).filter(models.Task.name == name).first()

    def fetch_all(self, skip: int = 0, limit: int = 100):
        task_list =  self.db.query(models.Task).offset(skip).limit(limit).all()
        task_list = [ task.dict() for task in task_list]
        return task_list

    async def delete(self,item_id: str):
        db_item= self.db.query(models.Task).filter_by(id=item_id).first()
        self.db.delete(db_item)
        self.db.commit()


    async def update(self, item_data):
        updated_item = self.db.merge(item_data)
        self.db.commit()
        return updated_item

task_repository = TaskRepository()
