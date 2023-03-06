import contextlib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.database.config.credentials import RDSCredentials
from src.tools import SingletonMeta

Base = declarative_base()


class DBManager(metaclass=SingletonMeta):
    def __init__(self):
        self.set_config()
        self.set_engine()
        self.factory_session()

    def set_config(self):
        self.config = RDSCredentials()

    def set_engine(self):
        self.engine = create_engine(self.config.get_url())

    def factory_session(self):
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def get_session(self):
        try:
            db = self.SessionLocal()
            yield db
        finally:
            db.close()

    @contextlib.contextmanager
    def get_session_with_ctx(self):
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
