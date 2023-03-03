from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import DDL

import src.database as dbmanager
from src import app
from src.database import DBManager
from src.database.dbconfig import RDSCredentials


@pytest.fixture
def rds_credentials_mock(mocker):
    mock = mocker.Mock(spec=RDSCredentials)
    mock.db_user = "test_user"
    mock.db_pass = "test_password"
    mock.db_host = "test_host"
    mock.db_database = "test_database"
    mock.get_url.return_value = "sqlite:///tests/db/test.db"

    mocker.patch.object(dbmanager, "RDSCredentials", return_value=mock)
    database = DBManager()
    database.set_config()
    database.set_engine()
    database.factory_session()

    # Base.metadata.create_all(bind=database.engine)

    return mock


@pytest.fixture(scope="session")
def client():

    return TestClient(app)


@pytest.fixture
def db(engine):
    ddl_gestao = DDL("CREATE SCHEMA IF NOT EXISTS gestao")
    ddl_cadastro = DDL("CREATE SCHEMA IF NOT EXISTS cadastro")

    with engine.connect() as conn:
        conn.execute(ddl_gestao)
        conn.execute(ddl_cadastro)
    return Mock()
