import logging
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database import DBManager, models, schemas
from src.database.entity.entities import EntitiesRbac

logger = logging.getLogger()
logger.setLevel(logging.INFO)

router = APIRouter()
auth_scheme = HTTPBearer()

entities = EntitiesRbac()
UserEntity = entities.get_entity("User")


class UserCreateSchema(BaseModel):
    idef_user: str
    nom_orig_usua: str


database = DBManager()


@router.get("/users", response_model=List[schemas.UserSchema])
def read_users(
    db: Session = Depends(database.get_session),
):
    users = db.query(models.User).all()
    return users


@router.post("/user", response_model=schemas.UserSchema)
def create_user(
    user: UserCreateSchema,
    db: Session = Depends(database.get_session),
):
    model = UserEntity["models"]["Table"]
    user = model(**user.dict())
    db.add(user)
    db.commit()
    return user
