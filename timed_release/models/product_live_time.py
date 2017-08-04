"""Product Live Time Model CRUD operation."""

from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import Time

from timed_release import config
from timed_release.connectors import sql


class ProductLiveTime(sql.base_model):
    """Table definition for product_live_time table."""

    __tablename__ = 'product_live_time'

    product_id = Column(
        'product_id', Integer, primary_key=True, nullable=False)
    time_of_day_product = Column(Time, nullable=False)
    time_zone = Column(Enum(*config.TIME_ZONES), nullable=False)
    store_id = Column(Integer, nullable=True)
