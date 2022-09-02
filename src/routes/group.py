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
authz_group = Authorizer("Group")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class GroupRequestSchema(BaseModel):
    nom_grup_usua: str
    des_grup_usua: str


@router.get("/groups", response_model=List[schemas.GroupSchema])
def read_groups(token=Depends(auth_scheme), db: Session = Depends(get_db)):
    if authz_group.authorize(2, token):
        try:
            groups = crud.get_groups(db)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return groups
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Usuario sem acesso a funcionalidade"},
        )


@router.post("/group", response_model=schemas.GroupSchema)
def create_group(
    group: GroupRequestSchema,
    token=Depends(auth_scheme),
    db: Session = Depends(get_db),
):
    if authz_group.authorize(1, token):
        try:
            response = crud.create_group(db, group)
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


@router.put("/group/{id_group}", response_model=schemas.GroupSchema)
def update_group(
    id_group: int,
    group: GroupRequestSchema,
    token=Depends(auth_scheme),
    db: Session = Depends(get_db),
):
    if authz_group.authorize(3, token):
        try:
            response = crud.update_group(db, id_group, group)
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


@router.delete("/group/{id_group}")
def delete_group(
    id_group: int, token=Depends(auth_scheme), db: Session = Depends(get_db)
):
    if authz_group.authorize(4, token):
        try:
            crud.delete_group(db, id_group)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return {f"Group {id_group} deleted!"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Usuario sem acesso a funcionalidade"},
        )
