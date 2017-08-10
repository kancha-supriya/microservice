"""Product Live Time Model CRUD operation."""

from oto import response

from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import Time

from timed_release import config
from timed_release.connectors import sql
from timed_release.constants import error


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
def get_product_live_time_details(product_id):
    """Get all information of product live time for given product id.

    Args:
        product_id (int)

    Return:
        response.Response: contaning dict or errors
    """
    with sql.db_session() as session:
        product_live_time = session.query(ProductLiveTime).get(product_id)
        if not product_live_time:
            return response.create_not_found_response(
                error.ERROR_CODE_PRODUCT_NOT_FOUND.format(product_id))

        return response.Response(message=product_live_time.to_dict())
