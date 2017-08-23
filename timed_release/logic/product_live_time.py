"""Product Live Time Logic CRUD operation."""

from oto import response

from timed_release.constants import error
from timed_release.models import product_live_time
from timed_release.validation import validators


def get_product_live_time_details(product_id):
    """Check if product id exist in product live table and return it.

    Args:
        product_id (str): Product id to fetch Spotify product live time.

    Return:
        response.Response: product live time details on successful fetch
        or error response.
    """
    if not validators.is_digit_and_non_zero(product_id):
        return response.create_error_response(
            code=error.ERROR_CODE_BAD_REQUEST,
            message=error.ERROR_MESSAGE_INTEGER_NON_NEGATIVE.format(
                product_id))
    return product_live_time.get_product_live_time_details(product_id)


def create_product_live_time_detail(timed_release_data):
    """Create product live time details.

    Args:
        timed_release_data (dict): Timed release data to create.

    Returns:
        response.Response: Message contains dict describing product live time
        details, or validation message.
    """
    product_id = timed_release_data.get('product_id')
    time_of_day_product = timed_release_data.get('time_of_day_product')
    time_zone = timed_release_data.get('time_zone')
    store_id = timed_release_data.get('store_id')

    return product_live_time.create_product_live_time_details(
        product_id, time_of_day_product, time_zone, store_id)


def update_product_live_time(product_id, data):
    """Update product live time details.

    Args:
        product_id (str): Product id to update Spotify product live time.
        data (dict): Product live time data to be updated.

    Returns:
        response.Response: Response message upon successful update.
         or error Response otherwise.
    """
    if not validators.is_digit_and_non_zero(product_id):
        return response.create_error_response(
            code=error.ERROR_CODE_BAD_REQUEST,
            message=error.ERROR_MESSAGE_INTEGER_NON_NEGATIVE.format(
                product_id))

    validation_error = validators.validate_timed_release_dataset(
        data, data.keys())
    if validation_error:
        return response.create_error_response(
            code=error.ERROR_CODE_BAD_REQUEST, message=validation_error)
    return product_live_time.update_product_live_time_details(product_id, data)
