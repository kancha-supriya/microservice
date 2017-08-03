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
from werkzeug.exceptions import BadRequest

from timed_release import config
from timed_release.api import app
from timed_release.constants import error
from timed_release.logic import hello
from timed_release.logic import product_live_time


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


@app.route('/product/<product_id>', methods=['GET'])
def get_product_live_detail_by_id(product_id):
    """Get product live time details for given product id.

    Args:
        product_id (str): Product id to fetch Spotify product live time.

    Returns:
        flask.response: Response contains dict describing product live time
        details, or validation message.
    """
    return flaskify(product_live_time.get_product_live_time_details(
        product_id))


@app.route('/product', methods=['POST'])
def create_product_live_time_detail():
    """Save info about product live time detail.

    Returns:
        flask.Response: Response contains dict describing product live time
        details, or validation message.
    """
    valid_request_json = True
    try:
        timed_release_data = request.get_json()
        if not isinstance(timed_release_data, dict):
            valid_request_json = False
    except BadRequest:
        valid_request_json = False

    if not valid_request_json:
        return flaskify(response.create_error_response(
            code=error.ERROR_CODE_BAD_REQUEST,
            message=error.ERROR_MESSAGE_INVALID_BODY_MISSING))

    return flaskify(product_live_time.create_product_live_time_detail(
        timed_release_data))
