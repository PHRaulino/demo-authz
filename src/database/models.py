from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import relationship

from src.database import Base

tables_info = {
    "Actions": "tb_actions",
    "Functionalities": "functionalities",
    "Groups": "tb_groups",
    "Policies": "tb_policies",
    "Rel_Actio_Funct": "tb_rel_action_functionalities",
    "Rel_Group_Polic": "tb_rel_group_policies",
    "Rel_Polic_Actio_Funct": "tb_rel_polic_actio_funct",
    "Rel_Users_Group": "tb_rel_users_groups",
    "Users": "tb_users",
}


class SerializerUser(object):
    def serialize(self):
        user = {c: getattr(self, c) for c in inspect(self).attrs.keys()}
        policies = []
        groups = []
        for gr in user["groups"]:
            groups.append(gr.num_seqe_grup_usua)
            for policy in getattr(gr, "policies"):
                if policy.num_seqe_pltc not in policies:
                    policies.append(str(policy.num_seqe_pltc))
        user["policies"] = policies
        user["groups"] = groups
        return user


class SerializerPolicy(object):
    def serialize(self):
        policy_model = {
            c: getattr(self, c) for c in inspect(self).attrs.keys()
        }
        policy = {}
        for rra in policy_model["tbmn3007_rlmt_pltc_acao_fncd"]:
            if rra.num_seqe_fncd not in policy:
                policy[rra.num_seqe_fncd] = []
            policy[rra.num_seqe_fncd].append(str(rra.num_seqe_acao))
        return policy


users_groups = Table(
    f"{tables_info['Rel_Users_Group']}",
    Base.metadata,
    Column(
        "num_seqe_usua",
        Integer,
        ForeignKey(f"{tables_info['Users']}.num_seqe_usua"),
    ),
    Column(
        "num_seqe_grup_usua",
        Integer,
        ForeignKey(f"{tables_info['Groups']}.num_seqe_grup_usua"),
    ),
    Column(
        "dat_hor_atui",
        DateTime(),
        default=datetime.now(),
        onupdate=datetime.now(),
        nullable=False,
    ),
)

groups_policies = Table(
    f"{tables_info['Rel_Group_Polic']}",
    Base.metadata,
    Column(
        "num_seqe_pltc",
        Integer,
        ForeignKey(f"{tables_info['Policies']}.num_seqe_pltc"),
    ),
    Column(
        "num_seqe_grup_usua",
        Integer,
        ForeignKey(f"{tables_info['Groups']}.num_seqe_grup_usua"),
    ),
    Column(
        "dat_hor_atui",
        DateTime(),
        default=datetime.now(),
        onupdate=datetime.now(),
        nullable=False,
    ),
)

Functionality_actions = Table(
    f"{tables_info['Rel_Actio_Funct']}",
    Base.metadata,
    Column(
        "num_seqe_acao",
        Integer,
        ForeignKey(f"{tables_info['Actions']}.num_seqe_acao"),
    ),
    Column(
        "num_seqe_fncd",
        Integer,
        ForeignKey(f"{tables_info['Functionalities']}.num_seqe_fncd"),
    ),
    Column(
        "dat_hor_atui",
        DateTime(),
        default=datetime.now(),
        onupdate=datetime.now(),
        nullable=False,
    ),
)


class Policy(Base):
    __tablename__ = tables_info["Policies"]
    num_seqe_pltc = Column(Integer, primary_key=True)
    nom_pltc = Column(String(60))
    des_pltc = Column(String(100), nullable=False)
    ind_situ_pltc_ativ = Column(String(1), nullable=False)
    dat_hor_atui = Column(
        DateTime(),
        default=datetime.now(),
        onupdate=datetime.now(),
        nullable=False,
    )
    tbmn3007_rlmt_pltc_acao_fncd = relationship(
        "PolicyFunctionalityAction",
        back_populates=f"{tables_info['Policies']}",
        primaryjoin="{}.num_seqe_pltc == {}.num_seqe_pltc".format(
            "Policy", "PolicyFunctionalityAction"
        ),
    )

    def serialize(self):
        d = SerializerPolicy.serialize(self)
        return d


class Action(Base):
    __tablename__ = tables_info["Actions"]
    num_seqe_acao = Column(Integer, primary_key=True)
    nom_acao = Column(String(60), nullable=False)
    dat_hor_atui = Column(
        DateTime(),
        default=datetime.now(),
        onupdate=datetime.now(),
        nullable=False,
    )
    tbmn3007_rlmt_pltc_acao_fncd = relationship(
        "PolicyFunctionalityAction",
        back_populates=f"{tables_info['Actions']}",
        primaryjoin="{}.num_seqe_acao == {}.num_seqe_acao".format(
            "Action", "PolicyFunctionalityAction"
        ),
        lazy="dynamic",
    )


class Functionality(Base):
    __tablename__ = tables_info["Functionalities"]
    num_seqe_fncd = Column(Integer, primary_key=True)
    nom_fncd = Column(String(60), nullable=False)
    dat_hor_atui = Column(
        DateTime(),
        default=datetime.now(),
        onupdate=datetime.now(),
        nullable=False,
    )
    actions = relationship(
        "Action",
        secondary=tables_info["Rel_Actio_Funct"],
        backref=tables_info["Functionalities"],
        lazy="joined",
    )
    tbmn3007_rlmt_pltc_acao_fncd = relationship(
        "PolicyFunctionalityAction",
        back_populates=tables_info["Functionalities"],
        primaryjoin="{}.num_seqe_fncd == {}.num_seqe_fncd".format(
            "Functionality", "PolicyFunctionalityAction"
        ),
        lazy="dynamic",
    )


class PolicyFunctionalityAction(Base):
    __tablename__ = tables_info["Rel_Polic_Actio_Funct"]

    num_seqe_pltc = Column(
        Integer,
        ForeignKey(f"{tables_info['Policies']}.num_seqe_pltc"),
        primary_key=True,
    )
    num_seqe_fncd = Column(
        Integer,
        ForeignKey(f"{tables_info['Functionalities']}.num_seqe_fncd"),
        primary_key=True,
    )
    num_seqe_acao = Column(
        Integer,
        ForeignKey(f"{tables_info['Actions']}.num_seqe_acao"),
        primary_key=True,
    )
    dat_hor_atui = Column(
        DateTime(),
        default=datetime.now(),
        onupdate=datetime.now(),
        nullable=False,
    )

    tbmn3004_pltc_aces = relationship(
        "Policy", back_populates=tables_info["Rel_Polic_Actio_Funct"]
    )
    tbmn3002_fncd = relationship(
        "Functionality", back_populates=tables_info["Rel_Polic_Actio_Funct"]
    )
    tbmn3001_acao = relationship(
        "Action", back_populates=tables_info["Rel_Polic_Actio_Funct"]
    )


class Group(Base):
    __tablename__ = tables_info["Groups"]
    num_seqe_grup_usua = Column(Integer, primary_key=True)
    nom_grup_usua = Column(String(50))
    des_grup_usua = Column(String(150))
    dat_hor_atui = Column(
        DateTime(), default=datetime.now(), onupdate=datetime.now()
    )
    policies = relationship(
        "Policy",
        secondary=tables_info["Rel_Group_Polic"],
        backref=tables_info["Groups"],
        lazy="joined",
    )


class User(Base):
    __tablename__ = tables_info["Users"]
    num_seqe_usua = Column(Integer, primary_key=True)
    dat_hor_atui = Column(
        DateTime(), default=datetime.now(), onupdate=datetime.now()
    )
    nom_orig_usua = Column(String(255))
    idef_user = Column(String(255), unique=True)
    groups = relationship(
        "Group",
        secondary=tables_info["Rel_Users_Group"],
        backref=tables_info["Users"],
        lazy="joined",
    )

    def serialize(self):
        d = SerializerUser.serialize(self)
        return d
