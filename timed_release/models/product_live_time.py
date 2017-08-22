"""Product Live Time Model CRUD operation."""

from oto import response
from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import Time

from timed_release import config
from timed_release.connectors import sql
from timed_release.constants import error
from timed_release.constants import success
from timed_release.validation import validators


class ProductLiveTime(sql.base_model):
    """Table definition for product_live_time table."""

    __tablename__ = 'product_live_time'

    product_id = Column(
        'product_id', Integer, primary_key=True, nullable=False)
    time_of_day_product = Column(Time, nullable=False)
    time_zone = Column(Enum(*config.TIME_ZONES), nullable=False)
    store_id = Column(Integer, nullable=True)

    def to_dict(self):
        """Return a dictionary of a product_live_time."""
        return {
            'product_id': self.product_id,
            'time_of_day_product': str(self.time_of_day_product),
            'time_zone': self.time_zone,
            'store_id': self.store_id
        }


@sql.wrap_db_errors
def create_product_live_time_details(
        product_id, time_of_day_product, time_zone, store_id=None):
    """Create product live time details.

    Args:
        product_id (int): Unique identification for product.
        time_of_day_product (str): Time to product go live.
        time_zone (str): Time Zone to product go live.
        store_id (int): Unique identification for DMS.
    Returns:
        response.Response: Response dict of inserted product live time
        details or error.
    """
    timed_release_data = {
        'product_id': product_id,
        'time_of_day_product': time_of_day_product,
        'time_zone': time_zone,
        'store_id': store_id
    }

    required_fields = ['product_id', 'time_of_day_product', 'time_zone']
    validation_error = validators.validate_timed_release_dataset(
        timed_release_data, required_fields)

    if validation_error:
        return response.create_error_response(
            code=error.ERROR_CODE_BAD_REQUEST, message=validation_error)

    timed_release_data_to_add = ProductLiveTime(**timed_release_data)
    with sql.db_session() as session:
        session.add(timed_release_data_to_add)
        timed_release_insert_response = {'product': timed_release_data}
        return response.Response(message=timed_release_insert_response)


@sql.wrap_db_errors
def get_product_live_time_details(product_id):
    """Get all information of product live time for given product id.

    Args:
        product_id (int): Product id to fetch Spotify product live time.

    Return:
        response: message containing data upon successful query.
            error Response message otherwise.
    """
    with sql.db_session() as session:
        product_live_time = session.query(ProductLiveTime).get(product_id)
        if not product_live_time:
            return response.create_not_found_response(
                error.ERROR_MESSAGE_PRODUCT_NOT_FOUND.format(product_id))

        return response.Response(message=product_live_time.to_dict())


@sql.wrap_db_errors
def update_product_live_time_details(product_id, data):
    """Update information of product live time for given product id.

    Args:
        product_id (int): Product id to update product live time details.
        data (dict): Product live time data to be updated.

    Return:
        response.Response: Response message upon successful update.
        error Response message otherwise.
    """
    with sql.db_session() as session:
        affected_row_count = session.query(ProductLiveTime).filter(
            ProductLiveTime.product_id == product_id).update(data)

        if not affected_row_count:
            return response.create_not_found_response(
                error.ERROR_MESSAGE_PRODUCT_NOT_FOUND.format(product_id))

        return response.Response(
            message=success.UPDATE_SUCCESS_MESSAGE.format(product_id))
