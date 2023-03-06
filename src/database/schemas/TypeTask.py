from datetime import datetime

from pydantic import BaseModel

from src.database.config.mapper import Mapper

mapper = Mapper()
TypeTaskTable = mapper.get_entity("TypeTask")


class TypeTaskSchema(BaseModel):
    id_type: int
    nom_type: str
    desc_type: str
    dat_hor_atui: datetime

    class Config:
        orm_mode = True


TypeTaskTable.set_schema("Table", TypeTaskSchema)
