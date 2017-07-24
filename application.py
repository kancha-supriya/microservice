"""Application."""

from raven.contrib import flask

from app_name import api
from app_name import config
from app_name import handlers  # noqa


if config.SENTRY:
    api.app.config['SENTRY_DSN'] = config.SENTRY
    flask.Sentry(api.app)

app = api.app
