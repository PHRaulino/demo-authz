from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base
from src.database.config.mapper import Mapper

mapper = Mapper()
TaskTable = mapper.get_entity("Task")
ListTaskTypeTable = mapper.get_entity("ListTaskType")


class Task(Base):
    __tablename__ = TaskTable.short_name
    __table_args__ = {"schema": TaskTable.schema}
    id_task = Column(Integer, primary_key=True)
    desc_task = Column(String(50))
    status = Column(String(150))
    dat_hor_atui = Column(
        DateTime(), default=datetime.now(), onupdate=datetime.now()
    )
    lists_tasks_types = relationship(
        "ListTaskType",
        back_populates="tasks",
        primaryjoin="{}.id_task == {}.id_task".format("Task", "ListTaskType"),
    )


TaskTable.set_model("Table", Task)
