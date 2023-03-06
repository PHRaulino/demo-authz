import os

os.environ["ENVIRONMENT"] = "local"
os.environ["SK_DATABASE_USER"] = "root"
os.environ["SK_DATABASE_PASS"] = "mysql_pass"
os.environ["SK_DATABASE_ENDPOINT"] = "localhost:3306"
os.environ["DATABASE_AUTHZ"] = "db0"
os.environ["CONF_PATH"] = "tests/db/config_tables.json"
