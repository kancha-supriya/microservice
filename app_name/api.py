"""Application.

The API application is a `flask` application. It provides simple features such
as registering a url for a specific handlers.
"""

from flask import Flask
from owslogger import flask_logger
from owsrequest import flask_request

from app_name import config


app = Flask(config.SERVICE_NAME)
flask_logger.setup(
    app, config.LOGGER_DSN, config.ENVIRONMENT, config.LOGGER_NAME,
    config.LOGGER_LEVEL, config.SERVICE_NAME, config.SERVICE_VERSION,
    exclude_paths=[config.HEALTH_CHECK])
flask_request.setup(app, config.ENVIRONMENT)
