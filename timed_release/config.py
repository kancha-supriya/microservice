"""Application configuration."""

import logging
import os

import newrelic.agent


# Service information
SERVICE_NAME = 'ows-app-name'
SERVICE_VERSION = '1.0.0'

# Production environment
PROD_ENVIRONMENT = 'prod'
DEV_ENVIRONMENT = 'dev'
QA_ENVIRONMENT = 'qa'
ENVIRONMENT = os.environ.get('Environment', DEV_ENVIRONMENT)

if ENVIRONMENT == PROD_ENVIRONMENT:
    newrelic.agent.initialize('newrelic.ini')

# Errors and loggers
SENTRY = os.environ.get('SENTRY_DSN') or None
LOGGER_DSN = os.environ.get('LOGGER_DSN')
LOGGER_LEVEL = logging.INFO
LOGGER_NAME = 'ows1'

# Generic handlers
HEALTH_CHECK = '/hello/'
