from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base
from src.database.config.mapper import Mapper

mapper = Mapper()
TypeTaskTable = mapper.get_entity("TypeTask")
ListTaskTypeTable = mapper.get_entity("ListTaskType")


class TypeTask(Base):
    __tablename__ = TypeTaskTable.short_name
    __table_args__ = {"schema": TypeTaskTable.schema}
    id_type = Column(Integer, primary_key=True)
    nom_type = Column(String(50))
    desc_type = Column(String(150))
    dat_hor_atui = Column(
        DateTime(), default=datetime.now(), onupdate=datetime.now()
    )
    lists_tasks_types = relationship(
        "ListTaskType",
        back_populates="types",
        primaryjoin="{}.id_type == {}.id_type".format(
            "TypeTask", "ListTaskType"
        ),
    )


TypeTaskTable.set_model("Table", TypeTask)
