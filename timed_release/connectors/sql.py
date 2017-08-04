"""DB Connector.

Manages interactions with database schema.
"""

from contextlib import contextmanager
import functools

from oto import response
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import exc
from sqlalchemy import pool
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from timed_release import config
from timed_release.connectors import sentry


def get_engine():
    """Create engine based on config settings."""
    if config.POOL_CLASS == pool.QueuePool:
        _db_engine = create_engine(
            config.RDS_DB_URL, pool_size=config.POOL_SIZE,
            max_overflow=config.POOL_MAX_OVERFLOW,
            pool_recycle=config.POOL_RECYCLE_MS)
        if config.POOL_PRE_PING:
            @event.listens_for(_db_engine, 'engine_connect')
            def ping_connection(connection, branch):
                """Wrapper around ping connection."""
                _ping_connection(connection, branch)
        return _db_engine
    return create_engine(config.RDS_DB_URL, poolclass=config.POOL_CLASS)

db_engine = get_engine()

db_session_maker = sessionmaker(bind=db_engine)

base_model = declarative_base()


def _ping_connection(connection, branch):
    """Ping database connection after engine_connect event.

    This function is copied verbatim from
    http://docs.sqlalchemy.org/en/latest/core/pooling.html
    """
    if branch:
        # "branch" refers to a sub-connection of a connection,
        # we don't want to bother pinging on these.
        return

    # turn off "close with result".  This flag is only used with
    # "connectionless" execution, otherwise will be False in any case
    save_should_close_with_result = connection.should_close_with_result
    connection.should_close_with_result = False

    try:
        # run a SELECT 1.   use a core select() so that
        # the SELECT of a scalar value without a table is
        # appropriately formatted for the backend
        connection.scalar(select([1]))
    except exc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception.  It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        if err.connection_invalidated:
            # run the same SELECT again - the connection will re-validate
            # itself and establish a new connection.  The disconnect detection
            # here also causes the whole connection pool to be invalidated
            # so that all stale connections are discarded.
            connection.scalar(select([1]))
        else:
            raise
    finally:
        # restore "close with result"
        connection.should_close_with_result = save_should_close_with_result


@contextmanager
def db_session():
    """Provide a transactional scope around a series of operations.

    Taken from http://docs.sqlalchemy.org/en/latest/orm/session_basics.html
    This handles rollback and closing of session, so there is no need
    to do that throughout the code.

    Usage:
        with db_session() as session:
            session.execute(query)
    """
    session = db_session_maker()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def wrap_db_errors(function):
    """Decorate the given function with logic to handle SQLAlchemy errors.

    If a SQLAlchemy exception is thrown, it will be caught and logged and the
    function will return a fatal response.

    Args:
        function (func): the function to decorate

    Returns:
        func: function decorated with error-handling logic
    """
    @functools.wraps(function)
    def call_function_with_error_handling(*args, **kwargs):
        try:
            function_return = function(*args, **kwargs)
        except exc.SQLAlchemyError as exception:
            sentry.sentry_client.captureMessage(exception, stack=True)
            return response.create_fatal_response()

        return function_return
    return call_function_with_error_handling
