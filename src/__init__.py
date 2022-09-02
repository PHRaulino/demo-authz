import logging

from fastapi import FastAPI
from starlette.responses import FileResponse

from src.routes import (
    action,
    functionality,
    group,
    health,
    policy,
    relationship,
    user,
    version,
)
from src.tools import environ, log_utils

if environ("ENV") != "local":
    log_utils.setup_custom_logger("root")
    log_utils.setup_custom_logger("gunicorn.access")
    log_utils.setup_custom_logger("gunicorn.error")
    logger = logging.getLogger("root")
    logger.propagate = False

app = FastAPI()
favicon_path = "src/assets/favicon.ico"


@app.get("/favicon.ico")
async def favicon():
    return FileResponse(favicon_path)


app.include_router(version.router, tags=["Version"])
app.include_router(user.router, tags=["User"])
app.include_router(group.router, tags=["Group"])
app.include_router(policy.router, tags=["Policies"])
app.include_router(action.router, tags=["Action"])
app.include_router(functionality.router, tags=["Functionality"])
app.include_router(relationship.router, prefix="/relationship")
app.include_router(health.router, tags=["Health Check"])
