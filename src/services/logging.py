from __future__ import annotations
# Needs https://www.python.org/dev/peps/pep-0563/
import sys

import loguru
from models.settings import get_settings

__DEFAULT_LOGGER_NAME = "stream.tracker"


def get_logger(logger_name: str = __DEFAULT_LOGGER_NAME) -> loguru.Logger:
    settings = get_settings()
    config = {
        "handlers": [
            {"sink": sys.stdout, "colorize": True, "level": settings.log_level,
                "enqueue": True,  "serialize": False, "format": "[<level>{level}</level>] {time} - {module} - {name} - {message}"}
        ]
    }

    loguru.logger.configure(**config)
    return loguru.logger.bind(name=logger_name)
