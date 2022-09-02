from platform import python_version

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def version_python():
    return {"python_version": python_version()}
