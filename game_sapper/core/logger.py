import logging
import sys
import typing

from loguru import logger

if typing.TYPE_CHECKING:
    from core.componets import Application

# config = {
#     "handlers": [
#         {"sink": "error.log", "serialize": True, "level": "ERROR"},
#     ],
# }


def setup_logging(app: "Application") -> None:
    if app.settings.logging_guru:
        # logger.configure(**config)
        logger.add(
            sys.stderr,
            level=app.settings.logging_level,
            backtrace=True,
            diagnose=True,
        )
        app.logger = logger
    else:
        logging.basicConfig(level=app.settings.logging_level)
    app.logger.info("Starting logging")
