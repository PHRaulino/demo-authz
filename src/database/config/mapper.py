import json
from functools import partial
from typing import Callable, List, Type

from pydantic import BaseModel

from src.database import Base
from src.tools import SingletonMeta, environ

Func = Callable[..., any]


class EntityTable:
    def __init__(self, name, long_name, short_name, schema) -> None:
        self.name = name
        self.long_name = long_name
        self.short_name = short_name
        self.schema = schema
        self.models: List[Type[Base]] = {}
        self.schemas: List[Type[BaseModel]] = {}
        self.functions: List[Func] = {}

    def set_schema(self, name: str, schema: Type[Base]):
        self.schemas[name] = schema

    def set_model(self, name: str, model: Type[BaseModel]):
        self.models[name] = model

    def set_function(self, name: str, function: Func):
        setattr(self, name, partial(function, self))

    def get_schema(self, name: str) -> Type[BaseModel]:
        return self.schemas[name]

    def get_model(self, name: str) -> Type[Base]:
        return self.models[name]

    def get_function(self, name: str) -> Func:
        return getattr(self, name)


class Mapper(metaclass=SingletonMeta):
    def __init__(self):
        self.set_config_path(environ("CONF_PATH"))
        self.entities: List[EntityTable] = {}
        self.get_conf_tables()
        self.update_tables()

    def set_config_path(self, path):
        self.config_path = path

    def get_db_schema(self, schema):
        return self.schemas[schema]

    def get_conf_tables(self):
        self.config = json.load(
            open(self.config_path, mode="r", encoding="utf-8")
        )

    def update_tables(self):
        for name, long_name in self.config.items():
            has_schema = "." in long_name
            short_name = long_name.split(".")[1] if has_schema else long_name
            schema = long_name.split(".")[0] if has_schema else None
            self.entities[name] = EntityTable(
                name, long_name, short_name, schema
            )

    def get_entity(self, key) -> EntityTable:
        return self.entities[key]

    def add_model(self, key, name, model):
        self.entities[key]["models"][name] = model
