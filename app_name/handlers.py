"""Application Handlers.

Requests are redirected to handlers, which are responsible for getting
information from the URL and passing it down to the logic layer. The way
each layer talks to each other is through Response objects which defines the
type status of the data and the data itself.

Please note: the Orchard uses the term handlers over views as convention
for clarity

See:
    oto.response for more details.
"""


from flask import g
from flask import jsonify
from flask import request

from oto import response
from oto.adaptors.flask import flaskify

from app_name import config
from app_name.api import app
from app_name.logic import hello


@app.route('/', methods=['GET'])
def hello_world():
    """Hello World with an optional GET param "name"."""
    name = request.args.get('name', '')
    return flaskify(hello.say_hello(name))


@app.route('/<username>', methods=['GET'])
def hello_world_username(username):
    """Hello World on /<username>.

    Args:
        username (str): the user's username.
    """
    return flaskify(hello.say_hello(username))


@app.route(config.HEALTH_CHECK, methods=['GET'])
def health():
    """Check the health of the application."""
    return jsonify({'status': 'ok'})


@app.errorhandler(500)
def exception_handler(error):
    """Default handler when uncaught exception is raised.

    Note: Exception will also be sent to Sentry if config.SENTRY is set.

    Returns:
        flask.Response: A 500 response with JSON 'code' & 'message' payload.
    """
    message = (
        'The server encountered an internal error '
        'and was unable to complete your request.')
    g.log.exception(error)
    return flaskify(response.create_fatal_response(message))
