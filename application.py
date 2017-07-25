"""Application."""

from raven.contrib import flask

from timed_release import api
from timed_release import config
from timed_release import handlers  # noqa


if config.SENTRY:
    api.app.config['SENTRY_DSN'] = config.SENTRY
    flask.Sentry(api.app)

app = api.app
