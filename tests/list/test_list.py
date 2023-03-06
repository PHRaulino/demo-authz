import random
import timeit

from src.database.config.mapper import Mapper


def test_get_list_without_task_v1(client, db):
    mapper = Mapper()
    ListTable = mapper.get_entity("List")
    TaskTable = mapper.get_entity("Task")
    TypeTaskTable = mapper.get_entity("TypeTask")
    ListTaskTypeTable = mapper.get_entity("ListTaskType")

    type_task = TypeTaskTable.create_item(
        db, {"nom_type": "Work", "desc_type": "Work type"}
    )

    for i in range(1000):
        ListTable.create_item(db, {"desc_list": f"List {i}"})

    for i in range(1000):
        item_task = TaskTable.create_item(
            db, {"desc_task": f"Task {i}", "status": "Done"}
        )
        lists = ListTable.get_all(db)
        if lists:
            random_list = random.choice(lists)
            ListTaskTypeTable.create_item(
                db,
                {
                    "id_list": random_list.id_list,
                    "id_task": item_task.id_task,
                    "id_type": type_task.id_type,
                },
            )

    t1 = timeit.timeit(
        lambda: ListTable.get_list_without_task_handwork(db=db), number=100
    )
    t2 = timeit.timeit(
        lambda: ListTable.get_list_without_task_subquery(db=db), number=100
    )
    time1 = f"Tempo de execução da função: {t1:.5f} segundos"
    time2 = f"Tempo de execução da função: {t2:.5f} segundos"
    print(time1)
    print(time2)
    print("Finish")
