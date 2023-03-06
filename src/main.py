import logging

from fastapi import FastAPI
from starlette.responses import FileResponse

from src.database.functions.default import crud_router
from src.routes import version
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
app.include_router(crud_router())
