"""Application configuration."""

import logging
import os

import newrelic.agent
from sqlalchemy.pool import QueuePool
from sqlalchemy.pool import StaticPool


# Service information
SERVICE_NAME = 'ows-timed-release'
SERVICE_VERSION = '1.0.0'

# Production environment
PROD_ENVIRONMENT = 'prod'
DEV_ENVIRONMENT = 'dev'
QA_ENVIRONMENT = 'qa'
TEST_ENVIRONMENT = 'test'
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

# Database config
RDS_DB_URL = 'sqlite://'
POOL_CLASS = StaticPool

if ENVIRONMENT != TEST_ENVIRONMENT:
    RDS_DB_URL = os.environ.get('RDS_DB_URL', 'sqlite://')
    POOL_CLASS = QueuePool
    POOL_SIZE = 5
    POOL_RECYCLE_MS = 3600  # Avoids connections going stale
    POOL_MAX_OVERFLOW = -1
    POOL_PRE_PING = True

# Time zones of product live time
TIME_ZONES = ('local', 'GMT')

# Time format for time_of_day_product field
DEFAULT_TIME_FORMAT = '%H:%M:%S'
