import json

from src.tools import SingletonMeta


class EntitiesRbac(metaclass=SingletonMeta):
    def __init__(self):
        self.set_config_path("src/database/entity/config_tables.json")
        self.entities = {}
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
        for key, value in self.config.items():
            has_schema = "." in value
            table = value.split(".")[1] if has_schema else value
            schema = value.split(".")[0] if has_schema else None
            if key not in self.entities:
                self.entities[key] = {"table": {}, "models": {}}

            self.entities[key]["table"]["short_name"] = table
            self.entities[key]["table"]["name"] = value
            self.entities[key]["table"]["schema"] = schema

    def get_entity(self, key):
        return self.entities[key]

    def add_model(self, key, name, model):
        self.entities[key]["models"][name] = model
