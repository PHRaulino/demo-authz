from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..tools import AwsService, environ

if environ("ENV") != "local":
    aws = AwsService()
    secrets = aws.client_secrets()
    db_user = (
        secrets.get_secret_value(SecretId=environ("DB_USER"))["SecretString"],
    )
    db_pass = secrets.get_secret_value(SecretId=environ("DB_PASS"))[
        "SecretString"
    ]
    db_host = secrets.get_secret_value(SecretId=environ("DB_HOST"))[
        "SecretString"
    ]
else:
    db_user = environ("DB_USER")
    db_pass = environ("DB_PASS")
    db_host = environ("DB_HOST")

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(
    db_user,
    db_pass,
    db_host,
    environ("DB_DATABASE"),
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
