"""db.py.

Database level utility class for testing against timed_release model.
"""

from functools import wraps
import sys

from timed_release import config
from timed_release.connectors.sql import db_session_maker


DROP_TABLE_PRODUCT_LIVE_TIME = """
DROP TABLE IF EXISTS asset;
"""


CREATE_TABLE_PRODUCT_LIVE_TIME = """
CREATE TABLE product_live_time (
  product_id int(10) PRIMARY KEY,
  time_of_day_product varchar(200)),
  time_zone varchar(200),
  store_id int(10);
"""


def drop_product_live_time_table():
    """DROP command for product_live_time table."""
    with db_session_maker() as session:
        _exit_if_not_test_environment(session)
        session.execute(DROP_TABLE_PRODUCT_LIVE_TIME)


def create_product_live_time_table():
    """Create product_live_time table."""
    with db_session_maker() as session:
        _exit_if_not_test_environment(session)
        session.execute(DROP_TABLE_PRODUCT_LIVE_TIME)
        session.execute(CREATE_TABLE_PRODUCT_LIVE_TIME)


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
        create_product_live_time_table()

        try:
            function_return = function(*args, **kwargs)
        finally:
            drop_product_live_time_table()

        return function_return
    return call_function_within_db_context
