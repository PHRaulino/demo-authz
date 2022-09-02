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
auth_scheme = HTTPBearer()
authz_rel_user = Authorizer("Relationship_User")
authz_rel_group = Authorizer("Relationship_Group")
authz_rel_policy = Authorizer("Relationship_Policy")
authz_rel_functionality = Authorizer("Relationship_Functionality")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class GroupRelationshipSchema(BaseModel):
    id_group: int
    id_policy: int


class UserRelationshipSchema(BaseModel):
    idef_user: str
    id_group: int


class FunctionalityRelationshipSchema(BaseModel):
    id_functionality: int
    id_action: int


class PltcFncdAcaoRelationshipSchema(BaseModel):
    id_policy: int
    id_functionality: int
    id_action: int


@router.post("/user/group", response_model=schemas.UserSchema, tags=["User"])
def add_group(
    relationship: UserRelationshipSchema,
    token=Depends(auth_scheme),
    db: Session = Depends(get_db),
):
    if authz_rel_user.authorize(1, token):
        try:
            user = crud.rel_user_group(db, delete=False, **relationship.dict())
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


@router.delete("/user/group", response_model=schemas.UserSchema, tags=["User"])
def remove_group(
    relationship: UserRelationshipSchema,
    token=Depends(auth_scheme),
    db: Session = Depends(get_db),
):
    if authz_rel_user.authorize(4, token):
        try:
            user = crud.rel_user_group(db, delete=True, **relationship.dict())
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


@router.post(
    "/group/policy",
    response_model=schemas.GroupSchema,
    tags=["Group"],
)
def add_policy(
    relationship: GroupRelationshipSchema,
    token=Depends(auth_scheme),
    db: Session = Depends(get_db),
):
    if authz_rel_group.authorize(1, token):
        try:
            group = crud.rel_group_policy(
                db, delete=False, **relationship.dict()
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return group
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Usuario sem acesso a funcionalidade"},
        )


@router.delete(
    "/group/policy", response_model=schemas.GroupSchema, tags=["Group"]
)
def remove_policy(
    relationship: GroupRelationshipSchema,
    token=Depends(auth_scheme),
    db: Session = Depends(get_db),
):
    if authz_rel_group.authorize(4, token):
        try:
            group = crud.rel_group_policy(
                db, delete=True, **relationship.dict()
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return group
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Usuario sem acesso a funcionalidade"},
        )


@router.post(
    "/functionality/action",
    response_model=schemas.FunctionalitySchema,
    tags=["Functionality"],
)
def add_action(
    relationship: FunctionalityRelationshipSchema,
    token=Depends(auth_scheme),
    db: Session = Depends(get_db),
):
    if authz_rel_functionality.authorize(1, token):
        try:
            functionality = crud.rel_functionality_action(
                db, delete=False, **relationship.dict()
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return functionality
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Usuario sem acesso a funcionalidade"},
        )


@router.delete(
    "/functionality/action",
    response_model=schemas.FunctionalitySchema,
    tags=["Functionality"],
)
def remove_action(
    relationship: FunctionalityRelationshipSchema,
    token=Depends(auth_scheme),
    db: Session = Depends(get_db),
):
    if authz_rel_functionality.authorize(4, token):
        try:
            functionality = crud.rel_functionality_action(
                db, delete=True, **relationship.dict()
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return functionality
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Usuario sem acesso a funcionalidade"},
        )


@router.post(
    "/policy/functionality_action",
    tags=["Policies"],
)
def add_policy_functionality_action(
    relationship: PltcFncdAcaoRelationshipSchema,
    token=Depends(auth_scheme),
    db: Session = Depends(get_db),
):
    if authz_rel_policy.authorize(1, token):
        try:
            pltc_fncd_acao = crud.rel_policy_functionality_action(
                db, **relationship.dict()
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return pltc_fncd_acao
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Usuario sem acesso a funcionalidade"},
        )


@router.delete(
    "/policy/functionality_action",
    tags=["Policies"],
)
def remove_policy_functionality_action(
    relationship: PltcFncdAcaoRelationshipSchema,
    token=Depends(auth_scheme),
    db: Session = Depends(get_db),
):
    if authz_rel_policy.authorize(4, token):
        try:
            crud.delete_policy_functionality_action(db, **relationship.dict())
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": e.args[0]},
            )
        return {"Relationship Policy Functionality Action deleted!"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Usuario sem acesso a funcionalidade"},
        )
