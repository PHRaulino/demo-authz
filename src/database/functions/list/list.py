from sqlalchemy import func
from sqlalchemy.orm import Session

from src.database.config.mapper import EntityTable, Mapper

mapper = Mapper()
ListTable = mapper.get_entity("List")
ListTaskTypeTable = mapper.get_entity("ListTaskType")
ListTaskTypeModel = ListTaskTypeTable.get_model("Table")
TaskTable = mapper.get_entity("Task")
TaskModel = TaskTable.get_model("Table")


def get_list_without_task_handwork(table: EntityTable, db: Session):
    model = table.get_model("Table")

    lists = db.query(model).all()

    [
        list_model
        for list_model in lists
        if len(list(list_model.lists_tasks_types)) == 0
    ]


def get_list_without_task_subquery(table: EntityTable, db: Session):
    model = table.get_model("Table")

    subquery = (
        db.query(model.id_list)
        .join(ListTaskTypeModel)
        .join(TaskModel)
        .group_by(model.id_list)
        .having(func.count(TaskModel.id_task) > 0)
        .subquery()
    )

    # Selecionar as listas que não estão na subconsulta
    lists_without_tasks = (
        db.query(model)
        .outerjoin(ListTaskTypeModel)
        .outerjoin(TaskModel)
        .filter(model.id_list.notin_(subquery))
        .all()
    )
    return lists_without_tasks


ListTable.set_function(
    "get_list_without_task_subquery", get_list_without_task_subquery
)
ListTable.set_function(
    "get_list_without_task_handwork", get_list_without_task_handwork
)
