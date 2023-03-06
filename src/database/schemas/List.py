from datetime import datetime

from pydantic import BaseModel

from src.database.config.mapper import Mapper

mapper = Mapper()
ListTable = mapper.get_entity("List")


class ListSchema(BaseModel):
    id_list: int
    desc_list: str
    dat_hor_atui: datetime

    class Config:
        orm_mode = True


ListTable.set_schema("Table", ListSchema)
