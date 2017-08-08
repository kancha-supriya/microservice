from oto import response

from timed_release.models import product_live_time
from timed_release.constants import error


def check_timed_release_exits(product_id):
    """Checks if product id exits in product live table.

    Args:
        product_id (int)

    Return:
     response.Response = boolean value true if exits.
    """
    if not product_id.isdigit() or int(product_id) <= 0:
        return response.create_error_response(
            code=error.ERROR_CODE_BAD_REQUEST,
            message=error.ERROR_MESSAGE_INVALID_CHARACTER,
            status='400')

    return product_live_time.get_product_live_time_details(product_id)
