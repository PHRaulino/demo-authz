from datetime import datetime
from typing import List, Union

from pydantic import BaseModel


class ActionSchema(BaseModel):
    num_seqe_acao: int
    nom_acao: str
    dat_hor_atui: datetime

    class Config:
        orm_mode = True


class FunctionalitySchema(BaseModel):
    num_seqe_fncd: int
    nom_fncd: str
    dat_hor_atui: datetime
    actions: List[ActionSchema] = []

    class Config:
        orm_mode = True


class PolicyFunctionalityActionSchema(BaseModel):
    num_seqe_pltc: int
    num_seqe_acao: int
    num_seqe_fncd: int
    dat_hor_atui: datetime

    class Config:
        orm_mode = True


class PolicySchema(BaseModel):
    num_seqe_pltc: int
    nom_pltc: Union[str, None] = None
    des_pltc: str
    ind_situ_pltc_ativ: str
    dat_hor_atui: datetime
    tbmn3007_rlmt_pltc_acao_fncd: List[PolicyFunctionalityActionSchema] = []

    class Config:
        orm_mode = True


class GroupSchema(BaseModel):
    num_seqe_grup_usua: int
    nom_grup_usua: str
    des_grup_usua: str
    dat_hor_atui: datetime

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    num_seqe_usua: int
    dat_hor_atui: datetime
    nom_orig_usua: str
    idef_user: str
    groups: List[GroupSchema] = []

    class Config:
        orm_mode = True
