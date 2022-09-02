import logging

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database import SessionLocal, crud, schemas
from src.security import Authorizer

logger = logging.getLogger()
logger.setLevel(logging.INFO)

router = APIRouter()
auth_scheme = HTTPBearer()

authz_user = Authorizer("User")


def decode_token(token):
    return jwt.decode(token.credentials, options={"verify_signature": False})


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreateSchema(BaseModel):
    idef_user: str
    nom_orig_usua: str


@router.post("/user", response_model=schemas.UserSchema)
def create_user(
    user: UserCreateSchema,
    token=Depends(auth_scheme),
    db: Session = Depends(get_db),
):
    if authz_user.authorize(1, token):
        try:
            user = crud.create_user(db, user)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return user.serialize()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Usuario sem acesso a funcionalidade"},
        )


@router.get("/user", response_model=schemas.UserSchema)
def read_user(
    token=Depends(auth_scheme),
    db: Session = Depends(get_db),
):
    try:
        id_user = decode_token(token)["usuario"]
        user = crud.get_user(db, id_user).first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": e.args[0]},
        )
    return user.serialize()


@router.delete("/user/{id_user}")
def delete_user(
    idef_user: str, token=Depends(auth_scheme), db: Session = Depends(get_db)
):
    if authz_user.authorize(4, token):
        try:
            crud.delete_user(db, idef_user)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return {f"User {idef_user} deleted!"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Usuario sem acesso a funcionalidade"},
        )
