from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.database import Base
from src.database.config.mapper import Mapper

mapper = Mapper()
ListTaskTypeTable = mapper.get_entity("ListTaskType")
ListTable = mapper.get_entity("List")
TaskTable = mapper.get_entity("Task")
TypeTaskTable = mapper.get_entity("TypeTask")


class ListTaskType(Base):
    __tablename__ = ListTaskTypeTable.short_name
    __table_args__ = {"schema": ListTaskTypeTable.schema}
    id_list = Column(
        Integer,
        ForeignKey("{}.id_list".format(ListTable.long_name)),
        primary_key=True,
    )
    id_task = Column(
        Integer,
        ForeignKey("{}.id_task".format(TaskTable.long_name)),
        primary_key=True,
    )
    id_type = Column(
        Integer,
        ForeignKey("{}.id_type".format(TypeTaskTable.long_name)),
        primary_key=True,
    )
    dat_hor_atui = Column(
        DateTime(), default=datetime.now(), onupdate=datetime.now()
    )

    lists = relationship("List", back_populates="lists_tasks_types")
    tasks = relationship("Task", back_populates="lists_tasks_types")
    types = relationship("TypeTask", back_populates="lists_tasks_types")


ListTaskTypeTable.set_model("Table", ListTaskType)
