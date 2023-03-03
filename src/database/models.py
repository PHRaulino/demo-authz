from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from src.database import Base
from src.database.entity.entities import EntitiesRbac

entities = EntitiesRbac()
UserEntity = entities.get_entity("User")
UserGroupEntity = entities.get_entity("Rel_Users_Group")
GroupEntity = entities.get_entity("Group")


users_groups = Table(
    UserGroupEntity["table"]["short_name"],
    Base.metadata,
    Column(
        "num_seqe_usua",
        Integer,
        ForeignKey("{}.num_seqe_usua".format(UserEntity["table"]["name"])),
    ),
    Column(
        "num_seqe_grup_usua",
        Integer,
        ForeignKey(
            "{}.num_seqe_grup_usua".format(GroupEntity["table"]["name"])
        ),
    ),
    Column(
        "dat_hor_atui",
        DateTime(),
        default=datetime.now(),
        onupdate=datetime.now(),
        nullable=False,
    ),
    schema=UserGroupEntity["table"]["schema"],
)


class Group(Base):
    __tablename__ = GroupEntity["table"]["short_name"]
    __table_args__ = {"schema": GroupEntity["table"]["schema"]}
    num_seqe_grup_usua = Column(Integer, primary_key=True)
    nom_grup_usua = Column(String(50))
    des_grup_usua = Column(String(150))
    dat_hor_atui = Column(
        DateTime(), default=datetime.now(), onupdate=datetime.now()
    )


class User(Base):
    __tablename__ = UserEntity["table"]["short_name"]
    __table_args__ = {"schema": UserEntity["table"]["schema"]}
    num_seqe_usua = Column(Integer, primary_key=True)
    dat_hor_atui = Column(
        DateTime(), default=datetime.now(), onupdate=datetime.now()
    )
    nom_orig_usua = Column(String(255))
    idef_user = Column(String(255), unique=True)
    groups = relationship(
        "Group",
        secondary=UserGroupEntity["table"]["name"],
        backref=UserEntity["table"]["name"],
        lazy="joined",
    )


entities.add_model("User", "Table", User)
entities.add_model("Group", "Table", Group)
