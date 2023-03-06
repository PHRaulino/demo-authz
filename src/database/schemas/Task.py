from datetime import datetime

from pydantic import BaseModel

from src.database.config.mapper import Mapper

mapper = Mapper()
TaskTable = mapper.get_entity("Task")


class TaskSchema(BaseModel):
    id_task: int
    desc_task: str
    status: str
    dat_hor_atui: datetime

    class Config:
        orm_mode = True


TaskTable.set_schema("Table", TaskSchema)
