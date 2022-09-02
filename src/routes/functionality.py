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
authz_functionality = Authorizer("Functionality")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class FunctionalityRequestSchema(BaseModel):
    nom_fncd: str


@router.get(
    "/functionalities", response_model=List[schemas.FunctionalitySchema]
)
def read_functionalities(
    token=Depends(auth_scheme), db: Session = Depends(get_db)
):
    if authz_functionality.authorize(2, token):
        try:
            functionalities = crud.get_functionalities(db)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return functionalities
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Usuario sem acesso a funcionalidade"},
        )


@router.post("/functionality", response_model=schemas.FunctionalitySchema)
def create_functionality(
    functionality: FunctionalityRequestSchema,
    token=Depends(auth_scheme),
    db: Session = Depends(get_db),
):
    if authz_functionality.authorize(1, token):
        try:
            response = crud.create_functionality(db, functionality)
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


@router.delete("/functionality/{id_functionality}")
def delete_functionality(
    id_functionality: int,
    token=Depends(auth_scheme),
    db: Session = Depends(get_db),
):
    if authz_functionality.authorize(4, token):
        try:
            crud.delete_functionality(db, id_functionality)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return {f"Functionality {id_functionality} deleted!"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Usuario sem acesso a funcionalidade"},
        )
