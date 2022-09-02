import os

import boto3

from .singleton import SingletonMeta

env_map = {
    "ENV": "ENVIRONMENT",
    "DB_USER": "SK_DATABASE_USER",
    "DB_PASS": "SK_DATABASE_PASS",
    "DB_HOST": "SK_DATABASE_ENDPOINT",
    "DB_DATABASE": "DATABASE_AUTHZ",
}


def environ(name, default=""):
    return os.getenv(env_map.get(name, ""), default)


class AwsService(metaclass=SingletonMeta):
    def __init__(self):
        self.region_name = "sa-east-1"
        self.clients = {}

    def client(self, name):
        if name not in self.clients:
            self.clients[name] = boto3.client(
                name, region_name=self.region_name
            )
        return self.clients[name]

    def client_secrets(self):
        return self.client(name="secretsmanager")

    def client_load_balancers(self):
        return self.client(name="elbv2")
