import logging
from datetime import datetime

import pytz
from pythonjsonlogger import jsonlogger

local_tz = pytz.timezone("America/Sao_Paulo")
appName = "apirbac"


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(
            log_record, record, message_dict
        )
        if not log_record.get("timestamp"):
            log_record["timestamp"] = (
                datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(local_tz)
            )
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname
        if log_record["level"] == "WARNING":
            log_record["level"] = "WARN"

            log_record["appName"] = appName
        if "HTTP" in record.message:
            log_record["type"] = "Request"
            log_record["Endpoint"] = record.message.replace('"', "").split(
                " "
            )[3]
        else:
            log_record["type"] = "Log Api"


def setup_custom_logger(name):
    formatter = CustomJsonFormatter("%(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)
    logger.addHandler(handler)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.propagate = False
    logger.addHandler(handler)
