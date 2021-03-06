"""Test for DB connection."""
from sqlalchemy.exc import NoSuchColumnError

from timed_release.connectors import sql


def test_wrap_db_errors():
    """Test wrap_db_errors with no errors."""
    @sql.wrap_db_errors
    def no_exception():
        return True

    response = no_exception()
    assert response


def test_wrap_db_errors_with_error():
    """Test wrap_db_errors when it raises an exception."""
    @sql.wrap_db_errors
    def has_exception():
        raise NoSuchColumnError('column not found')

    response = has_exception()
    assert response.status == 500
