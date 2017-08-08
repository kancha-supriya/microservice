"""db.py.

Database level utility class for testing against timed_release model.
"""

import datetime
from functools import wraps
import sys

from timed_release import config
from timed_release.connectors.sql import base_model
from timed_release.connectors.sql import db_engine
from timed_release.connectors.sql import db_session_maker
from timed_release.connectors.sql import db_session
from timed_release.models import product_live_time


def create_all_tables():
    """Create database table for all model classes."""
    _exit_if_not_test_environment(db_session_maker())
    # Creates table for all model where base_model is inherited.
    base_model.metadata.create_all(db_engine)


def drop_all_tables():
    """Drop a database table for model classes."""
    _exit_if_not_test_environment(db_session_maker())
    # Drops table for all model where base_model is inherited.
    base_model.metadata.drop_all(db_engine)


def _exit_if_not_test_environment(session):
    """For safety, only run tests in test environment pointed to sqlite.

    Exit immediately if not in test environment or not pointed to sqlite.
    """
    if config.ENVIRONMENT != config.TEST_ENVIRONMENT:
        sys.exit('Environment must be set to {}.'.format(
            config.TEST_ENVIRONMENT))
    if 'sqlite' not in session.bind.url.drivername:
        sys.exit('Tests must point to sqlite database.')


def test_schema(function):
    """Create and tear down the test DB schema around a function call.

    This just creates the schema and does not seed data. Individual test cases
    can use factories to seed data as needed.
    Args:
        function (func): the function to be called after creating the test
        schema.
    Returns:
        Function: The decorated function.
    """
    @wraps(function)
    def call_function_within_db_context(*args, **kwargs):
        create_all_tables()

        try:
            function_return = function(*args, **kwargs)
        finally:
            drop_all_tables()

        return function_return
    return call_function_within_db_context


INSERT_DATA = [
    {
        'product_id': '12',
        'time_of_day_product': datetime.time(20, 30, 00),
        'time_zone': 'GMT',
        'store_id': 1
    }]


def insert_product_live_time_data():
    """Insert data to product_live_time table."""
    with db_session() as session:
        session.bulk_insert_mappings(
            product_live_time.ProductLiveTime, INSERT_DATA)
