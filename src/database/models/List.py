from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base
from src.database.config.mapper import Mapper

mapper = Mapper()
ListTable = mapper.get_entity("List")
ListTaskTypeTable = mapper.get_entity("ListTaskType")


class List(Base):
    __tablename__ = ListTable.short_name
    __table_args__ = {"schema": ListTable.schema}
    id_list = Column(Integer, primary_key=True)
    desc_list = Column(String(255))
    dat_hor_atui = Column(
        DateTime(), default=datetime.now(), onupdate=datetime.now()
    )
    lists_tasks_types = relationship(
        "ListTaskType",
        back_populates="lists",
        primaryjoin="{}.id_list == {}.id_list".format("List", "ListTaskType"),
    )


ListTable.set_model("Table", List)
