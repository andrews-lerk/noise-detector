import logging.config
from colorlog import ColoredFormatter


def setup_logging() -> None:
    log_format = (
        "%(cyan)s%(asctime)s.%(msecs)03d%(reset)s | "
        "[%(log_color)s%(levelname)s%(reset)s]: "
        "%(message_log_color)s%(message)s%(reset)s"
    )
    logging_schema = {
        "version": 1,
        "formatters": {
            "colored": {
                "()": "colorlog.ColoredFormatter",
                "format": log_format,
                "datefmt": "%Z %Y-%m-%d %H:%M:%S",
                "log_colors": {
                    'DEBUG': 'purple',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                },
                "secondary_log_colors": {
                    'message': {
                        'DEBUG': 'white',
                        'INFO': 'light_white',
                        'WARNING': 'yellow',
                        'ERROR': 'red',
                        'CRITICAL': 'red,bg_white',
                    }
                },
                "style": "%"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "colored",
                "level": "DEBUG"
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False
            }
        },
    }
    logging.config.dictConfig(logging_schema)
