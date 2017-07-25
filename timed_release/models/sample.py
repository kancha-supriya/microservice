"""Model Sample.

This is just a model sample. It depends on which database you want to use but
basically make sure this file only contains methods and classes that are
related to this model.
"""

from oto import response
from owsrequest import request


class Model:
    """Your awesome model."""

    pass


def get_model_for_id(model_id):
    """Get a model by its id.

    Note:
        This is just an example on how to do a request from a microservice
        to another microservice using the owsrequest.request module. The module
        will create the HMAC for the request and will automatically calculate
        the next correlation id.

    Args:
        id (int): the id of the model.

    Returns:
        response.Response: the data of the model.
    """
    model = request.get('ows-microservice', '/resource')
    return response.Response(message=model.json(), status=model.status_code)
