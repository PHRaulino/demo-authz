from datetime import datetime

from pydantic import BaseModel

from src.database.config.mapper import Mapper

mapper = Mapper()
ListTaskTypeTable = mapper.get_entity("ListTaskType")


class ListTaskTypechema(BaseModel):
    id: int
    id_list: int
    id_task: int
    id_type: int
    dat_hor_atui: datetime

    class Config:
        orm_mode = True


ListTaskTypeTable.set_schema("Table", ListTaskTypechema)
