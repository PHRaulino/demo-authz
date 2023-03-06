from fastapi import APIRouter

from src.database.config.mapper import Mapper
from src.database.functions.default.crud import CRUDBase

mapper = Mapper()


def crud_router() -> APIRouter:
    router = APIRouter()
    for name, table in mapper.entities.items():
        crud = CRUDBase(table)
        router.include_router(
            crud.router,
            prefix="/{}".format(name.lower()),
            tags=[name],
        )
    return router
