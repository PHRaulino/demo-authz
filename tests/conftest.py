import pytest
from fastapi.testclient import TestClient

import src.database as dbmanager
from src.database import Base, DBManager
from src.database.config.credentials import RDSCredentials
from src.main import app

database = DBManager()


@pytest.fixture
def rds_credentials_mock(mocker):
    mock = mocker.Mock(spec=RDSCredentials)
    mock.db_user = "test_user"
    mock.db_pass = "test_password"
    mock.db_host = "test_host"
    mock.db_database = "test_database"
    mock.get_url.return_value = "sqlite:///tests/db/test.db"

    mocker.patch.object(dbmanager, "RDSCredentials", return_value=mock)
    database.set_config()
    database.set_engine()
    database.factory_session()

    return mock


@pytest.fixture(scope="function")
def db(rds_credentials_mock):
    Base.metadata.drop_all(bind=database.engine)
    Base.metadata.create_all(bind=database.engine)
    with database.get_session_with_ctx() as session:
        yield session


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
