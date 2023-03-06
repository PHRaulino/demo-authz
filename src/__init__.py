import glob
import os

sort = ["List.py", "Task.py", "TypeTask.py", "Relationship.py"]


def import_tables(src, sort=[]):
    if len(sort) == 0:
        files = glob.glob("{}/**/*.py".format(src), recursive=True)
    else:
        files = ["{}/{}".format(src, f) for f in sort]

    for file in [f for f in files if "__" not in f]:
        module = os.path.splitext(file)[0].replace("/", ".")
        __import__(module)


import_tables("src/database/models", sort)
import_tables("src/database/schemas")
import_tables("src/database/functions")
