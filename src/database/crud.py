from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import (
    Action,
    Functionality,
    Group,
    Policy,
    PolicyFunctionalityAction,
    User,
)


def get_user(db: Session, id_user: str):
    return db.query(User).filter(User.idef_user == id_user)


def get_group(db: Session, id_group: int):
    return db.query(Group).filter(Group.num_seqe_grup_usua == id_group)


def get_policy(db: Session, id_policy: int):
    return db.query(Policy).filter(Policy.num_seqe_pltc == id_policy)


def get_action(db: Session, id_action: int):
    return db.query(Action).filter(Action.num_seqe_acao == id_action)


def get_functionality(db: Session, id_functionality: int):
    return db.query(Functionality).filter(
        Functionality.num_seqe_fncd == id_functionality
    )


def create_user(db: Session, user: User):
    obj_user = User(**user.dict())
    db.add(obj_user)
    db.commit()
    db.refresh(obj_user)
    return obj_user


def delete_user(db: Session, id_user: str):
    get_user(db, id_user).delete()
    db.commit()


def get_policies(db: Session):
    return db.query(Policy).all()


def get_groups(db: Session):
    return db.query(Group).all()


def get_functionalities(db: Session):
    return db.query(Functionality).all()


def get_actions(db: Session):
    return db.query(Action).all()


def create_policy(db: Session, policy: Policy):
    obj_policy = Policy(**policy.dict())
    db.add(obj_policy)
    db.commit()
    db.refresh(obj_policy)
    return obj_policy


def update_policy(db: Session, id_policy: int, policy: Policy):
    query = get_policy(db, id_policy)
    query.update(policy.dict())
    db.commit()
    return query.first()


def switch_policy(db: Session, id_policy: int, policy):
    query = get_policy(db, id_policy)
    query.update(policy)
    db.commit()
    return query.first()


def delete_policy(db: Session, id_policy: int):
    get_policy(db, id_policy).delete()
    db.commit()


def create_group(db: Session, group: Group):
    obj_group = Group(**group.dict())
    db.add(obj_group)
    db.commit()
    db.refresh(obj_group)
    return obj_group


def update_group(db: Session, id_group: int, group: Group):
    query = get_group(db, id_group)
    query.update(group.dict())
    db.commit()
    return query.first()


def delete_group(db: Session, id_group: int):
    get_group(db, id_group).delete()
    db.commit()


def create_action(db: Session, action: Action):
    obj_action = Action(**action.dict())
    db.add(obj_action)
    db.commit()
    db.refresh(obj_action)
    return obj_action


def delete_action(db: Session, id_action: int):
    get_action(db, id_action).delete()
    db.commit()


def create_functionality(db: Session, funcionality: Functionality):
    obj_funcionality = Functionality(**funcionality.dict())
    db.add(obj_funcionality)
    db.commit()
    db.refresh(obj_funcionality)
    return obj_funcionality


def delete_functionality(db: Session, id_funcionality: int):
    get_functionality(db, id_funcionality).delete()
    db.commit()


def rel_user_group(db: Session, delete: bool, idef_user: str, id_group: int):
    user = get_user(db, idef_user).first()
    group = get_group(db, id_group).first()
    if delete:
        group_index = user.groups.index(group)
        user.groups.pop(group_index)
    else:
        user.groups.append(group)
        db.commit()
    return user


def rel_group_policy(db: Session, delete: bool, id_group: int, id_policy: int):
    group = get_group(db, id_group).first()
    policy = get_policy(db, id_policy).first()
    if delete:
        policy_index = group.policies.index(policy)
        group.policies.pop(policy_index)
    else:
        group.policies.append(policy)
        db.commit()
    return group


def rel_functionality_action(
    db: Session, delete: bool, id_functionality: int, id_action: int
):
    functionality = get_functionality(db, id_functionality).first()
    action = get_action(db, id_action).first()
    if delete:
        action_index = functionality.actions.index(action)
        functionality.actions.pop(action_index)
    else:
        functionality.actions.append(action)
        db.commit()
    return functionality


def rel_policy_functionality_action(
    db: Session,
    id_policy: int,
    id_functionality: int,
    id_action: int,
):
    pltc_fncd_acao = PolicyFunctionalityAction(
        num_seqe_pltc=id_policy,
        num_seqe_acao=id_action,
        num_seqe_fncd=id_functionality,
    )
    db.add(pltc_fncd_acao)
    db.commit()
    db.refresh(pltc_fncd_acao)
    return pltc_fncd_acao


def delete_policy_functionality_action(
    db: Session, id_policy: int, id_action: int, id_functionality: int
):
    db.query(PolicyFunctionalityAction).filter(
        and_(
            PolicyFunctionalityAction.num_seqe_pltc == id_policy,
            PolicyFunctionalityAction.num_seqe_fncd == id_functionality,
            PolicyFunctionalityAction.num_seqe_acao == id_action,
        )
    ).delete()
    db.commit()
