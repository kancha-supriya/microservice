"""Application configuration."""

import logging
import os

import newrelic.agent
from sqlalchemy.pool import NullPool
from sqlalchemy.pool import StaticPool


# Service information
SERVICE_NAME = 'ows-app-name'
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

# Database credentials
RDS_DB_CONNECTION_PROPERTIES = {
    'database': os.environ.get('RDS_MYSQL_DATABASE'),
    'host': os.environ.get('RDS_MYSQL_HOST'),
    'password': os.environ.get('RDS_MYSQL_PASSWORD'),
    'port': os.environ.get('RDS_MYSQL_PORT'),
    'user': os.environ.get('RDS_MYSQL_USER')
}

# Database config
if ENVIRONMENT == TEST_ENVIRONMENT:
    RDS_DB_URL = 'sqlite://'
    POOL_CLASS = StaticPool
else:
    RDS_DB_URL = (
        'mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8'
        .format(**RDS_DB_CONNECTION_PROPERTIES))
POOL_CLASS = NullPool
