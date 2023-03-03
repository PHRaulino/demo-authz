from src.tools import environ


class RDSCredentials:
    def __init__(self):
        self.db_user = environ("DB_USER")
        self.db_pass = environ("DB_PASS")
        self.db_host = environ("DB_HOST")
        self.db_database = environ("DB_DATABASE")

    def get_url(self):
        return "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(
            self.db_user, self.db_pass, self.db_host, self.db_database
        )
