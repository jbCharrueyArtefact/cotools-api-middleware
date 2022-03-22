from urllib import request
from pydantic import BaseModel
from logging.config import dictConfig
import logging
import json

log_format_dict = {"time": "%(asctime)s", "message": "%(message)s"}


class _LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "mycoolapp"
    LOG_FORMAT: str = json.dumps(log_format_dict)
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "GCP": {
            "()": "app.logger.googleLogger.GCPFormatter",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "gcp": {
            "formatter": "GCP",
            "class": "app.logger.googleLogger.GoogleLogger",
        },
    }
    loggers = {
        "cotools_log": {"handlers": ["gcp", "default"], "level": LOG_LEVEL}
    }


dictConfig(_LogConfig().dict())
logger = logging.getLogger("cotools_log")
