"""Unit tests for ProductLiveTime Model."""

from oto import status

from tests.testutils import db
from timed_release.models import product_live_time


def test_to_dict():
    """Test that the to dict function only returns the expected properties."""
    test_timed_release = product_live_time.ProductLiveTime(
        product_id='12',
        time_of_day_product='00:00:01',
        time_zone='GMT',
        store_id=1)
    expected_dict = {
        'product_id': test_timed_release.product_id,
        'time_of_day_product': test_timed_release.time_of_day_product,
        'time_zone': test_timed_release.time_zone,
        'store_id': test_timed_release.store_id}

    assert test_timed_release.to_dict() == expected_dict


@db.test_schema
def test_get_product_live_time_details_success():
    """Test to get product live time by product id."""
    data = {
        'product_id': 12,
        'time_of_day_product': '20:30:00',
        'time_zone': 'GMT',
        'store_id': 1
    }
    db.insert_product_live_time_data()
    response = product_live_time.get_product_live_time_details('12')
    assert response.message == data


@db.test_schema
def test_get_product_live_time_details_success_not_found():
    """Test that an existing product id is not found."""
    response = product_live_time.get_product_live_time_details('12')
    assert response.status == status.NOT_FOUND
