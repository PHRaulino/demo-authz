from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import DBManager
from src.database.config.mapper import EntityTable

database = DBManager()


def get_all(table: EntityTable, db: Session):
    model = table.get_model("Table")
    return db.query(model).all()


def get_item_by_id(table: EntityTable, db: Session, id):
    model = table.get_model("Table")
    return db.query(model).get(id)


def create_item(table: EntityTable, db: Session, payload):
    model = table.get_model("Table")
    instance = model(**payload)
    db.add(instance)
    db.commit()
    return instance


def delete_item(table: EntityTable, db: Session, id):
    model = table.get_model("Table")
    instance = db.query(model).get(id)
    db.delete(instance)
    db.commit()
    return instance


def update_item(table: EntityTable, db: Session, id, payload):
    model = table.get_model("Table")
    instance = db.query(model).get(id)
    for field, value in payload:
        setattr(instance, field, value)
    db.add(instance)
    db.commit()
    return instance


class CRUDBase:
    def __init__(self, table: EntityTable):
        self.model = table.get_model("Table")
        self.schema = table.get_schema("Table")

        self.router = APIRouter()
        self._register_routes()
        table.set_function("get_all", get_all)
        table.set_function("get_item_by_id", get_item_by_id)
        table.set_function("create_item", create_item)
        table.set_function("delete_item", delete_item)
        table.set_function("update_item", update_item)
        self.table = table

    def _register_routes(self):
        @self.router.get("/", response_model=List[self.schema])
        def read_all(db: Session = Depends(database.get_session)):
            return self.table.get_all(db)

        @self.router.get("/{id}", response_model=self.schema)
        def read_one(id: int, db: Session = Depends(database.get_session)):
            instance = self.table.get_item_by_id(db, id)
            if not instance:
                raise HTTPException(
                    status_code=404, detail="Resource not found"
                )
            return instance

        @self.router.post("/", response_model=self.schema)
        def create(
            payload: self.schema, db: Session = Depends(database.get_session)
        ):
            instance = self.table.create_item(db, payload.dict())
            return instance

        @self.router.put("/{id}", response_model=self.schema)
        def update(
            id: int,
            payload: self.schema,
            db: Session = Depends(database.get_session),
        ):
            instance = self.table.update_item(db, id, payload)
            if not instance:
                raise HTTPException(
                    status_code=404, detail="Resource not found"
                )
            return instance

        @self.router.delete("/{id}", response_model=self.schema)
        def delete(id: int, db: Session = Depends(database.get_session)):
            instance = self.table.delete_item(db, id)
            if not instance:
                raise HTTPException(
                    status_code=404, detail="Resource not found"
                )
            return instance
