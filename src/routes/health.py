from fastapi import APIRouter
from fastapi_health import health
from sqlalchemy.orm import Session

from src.database import SessionLocal

router = APIRouter()


def is_database_online():
    try:
        db: Session = SessionLocal()
        connection = db.connection()
        status = connection._still_open_and_dbapi_connection_is_valid
        db.close()
    except Exception:
        status = False
    return status


router.add_api_route("/health", health([is_database_online]))
