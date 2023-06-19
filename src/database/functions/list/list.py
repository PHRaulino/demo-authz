from sqlalchemy import func
from sqlalchemy.orm import Session

from src.database import DBManager
from src.database.config.mapper import EntityTable, Mapper

database = DBManager()
mapper = Mapper()
ListTable = mapper.get_entity("List")
ListTaskTypeTable = mapper.get_entity("ListTaskType")
ListTaskTypeModel = ListTaskTypeTable.get_model("Table")
TaskTable = mapper.get_entity("Task")
TaskModel = TaskTable.get_model("Table")


query = """
    SELECT *
    FROM tb_lists
    WHERE id_list NOT IN (
    SELECT DISTINCT id_list
    FROM tb_list_type_tasks
    )
"""


def cursor_to_dict(cols, result):
    results = []
    for row in result.fetchall():
        result_dict = {}
        for i in range(len(cols)):
            result_dict[cols[i]] = row[i]

        results.append(result_dict)

    return results


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


def get_list_without_task_with_session_cursor(table: EntityTable, db: Session):
    result = db.execute(query).cursor
    col_names = [desc[0] for desc in result.description]
    return cursor_to_dict(col_names, result)


def get_list_without_task_with_engine_cursor(table: EntityTable):
    with database.engine.connect() as db:
        result = db.execute(query).cursor
        col_names = [desc[0] for desc in result.description]
        resultado = cursor_to_dict(col_names, result)
    return resultado


ListTable.set_function(
    "get_list_without_task_subquery", get_list_without_task_subquery
)
ListTable.set_function(
    "get_list_without_task_handwork", get_list_without_task_handwork
)
ListTable.set_function(
    "get_list_without_task_with_session_cursor",
    get_list_without_task_with_session_cursor,
)
ListTable.set_function(
    "get_list_without_task_with_engine_cursor",
    get_list_without_task_with_engine_cursor,
)
