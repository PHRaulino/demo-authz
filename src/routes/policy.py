import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database import SessionLocal, crud, schemas
from src.security import Authorizer

logger = logging.getLogger()
logger.setLevel(logging.INFO)

router = APIRouter()
authz_policy = Authorizer("Policy")
auth_scheme = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PolicyRequestSchema(BaseModel):
    nom_pltc: str
    des_pltc: str
    ind_situ_pltc_ativ: str = "S"


@router.get("/policies")
def read_policies(db: Session = Depends(get_db)):
    try:
        query = crud.get_policies(db)
        policies = {}
        for policy in query:
            policies[policy.num_seqe_pltc] = policy.serialize()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": e.args[0]},
        )
    return policies


@router.post("/policy", response_model=schemas.PolicySchema)
def create_policy(
    policy: PolicyRequestSchema,
    db: Session = Depends(get_db),
):
    if authz_policy.authorize(1, token):
        try:
            response = crud.create_policy(db, policy)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return response


@router.put(
    "/policy/{id_policy}/activate", response_model=schemas.PolicySchema
)
def active_policy(id_policy: int, db: Session = Depends(get_db)):
    policy = {"ind_situ_pltc_ativ": "S"}
    if authz_policy.authorize(3, token):
        try:
            response = crud.switch_policy(db, id_policy, policy)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return response


@router.put(
    "/policy/{id_policy}/deactivate", response_model=schemas.PolicySchema
)
def deactivate_policy(id_policy: int, db: Session = Depends(get_db)):
    policy = {"ind_situ_pltc_ativ": "N"}
    if authz_policy.authorize(3, token):
        try:
            response = crud.switch_policy(db, id_policy, policy)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return response


@router.put("/policy/{id_policy}", response_model=schemas.PolicySchema)
def update_policy(
    id_policy: int,
    policy: PolicyRequestSchema,
    db: Session = Depends(get_db),
):
    if authz_policy.authorize(3, token):
        try:
            response = crud.update_policy(db, id_policy, policy)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return response


@router.delete("/policy/{id_policy}")
def delete_policy(id_policy: int, db: Session = Depends(get_db)):
    if authz_policy.authorize(4, token):
        try:
            crud.delete_policy(db, id_policy)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return {f"Policy {id_policy} deleted!"}
