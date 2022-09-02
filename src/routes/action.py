import logging
from typing import List

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
authz_action = Authorizer("Action")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ActionRequestSchema(BaseModel):
    nom_acao: str


@router.get("/actions", response_model=List[schemas.ActionSchema])
def read_actions(token=Depends(auth_scheme), db: Session = Depends(get_db)):
    if authz_action.authorize(2, token):
        try:
            actions = crud.get_actions(db)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return actions
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Usuario sem acesso a funcionalidade"},
        )


@router.post("/action", response_model=schemas.ActionSchema)
def create_action(
    action: ActionRequestSchema,
    token=Depends(auth_scheme),
    db: Session = Depends(get_db),
):
    if authz_action.authorize(1, token):
        try:
            response = crud.create_action(db, action)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Usuario sem acesso a funcionalidade"},
        )


@router.delete("/action/{id_action}")
def delete_action(
    id_action: int, token=Depends(auth_scheme), db: Session = Depends(get_db)
):
    if authz_action.authorize(4, token):
        try:
            crud.delete_action(db, id_action)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return {f"Action {id_action} deleted!"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Usuario sem acesso a funcionalidade"},
        )
