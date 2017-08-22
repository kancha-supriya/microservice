""""Test for Product Live Time Model CRUD operation."""

import datetime
from unittest.mock import MagicMock
from unittest.mock import patch
from oto import response
from oto import status as http_status

import pytest
from sqlalchemy.exc import SQLAlchemyError

from tests.testutils import db
from timed_release.constants import success
from timed_release.models import product_live_time
from timed_release.validation import validators


@db.test_schema
@pytest.mark.parametrize(
    'description, product_id, time_of_day_product, time_zone, store_id', [
        ('testing with GMT timezone', 2080166, datetime.time(20, 30, 00),
            'GMT', 286),
        ('testing with local timezone', 2080168, datetime.time(11, 45, 00),
            'local', 286)])
def test_create_product_live_time_details_success(
        description, product_id, time_of_day_product, time_zone, store_id,
        monkeypatch):
    """Test for create time release details with success."""
    request_body = {
        'product_id': product_id,
        'time_of_day_product': time_of_day_product,
        'time_zone': time_zone,
        'store_id': store_id
    }
    expected_response = {'product': request_body}

    # mocking validators validate_time method with result true
    monkeypatch.setattr(
        validators, 'validate_time',
        MagicMock(return_value=response.Response(message=True)))

    insert_response = product_live_time.create_product_live_time_details(
        product_id, time_of_day_product, time_zone, store_id)

    assert insert_response.status == http_status.OK
    assert insert_response.message == expected_response


@pytest.mark.parametrize(
    'description, product_id, time_of_day_product, time_zone, store_id', [
        ('testing with product_id is non integer', '2080166xyz', '20:30:00',
            'GMT', 286),
        ('testing with product_id has negative value', -2080166, '20:30:00',
            'GMT', 286),
        ('testing with invalid time', 2080169, '85:30:00', 'local', 286),
        ('testing with store_id is non integer', 2080168, '20:30:00', 'GMT',
            '286abc'),
        ('testing with store_id has negative value', 2080168, '20:30:00',
            'GMT', -286),
        ('testing with invalid time zone', 2080169, '20:33:00', 'UTC', 286)])
def test_create_product_live_time_details_validations(
        description, product_id, time_of_day_product, time_zone, store_id,
        monkeypatch):
    """Test for create product live time details with validations."""
    request_body = {
        'product_id': product_id,
        'time_of_day_product': time_of_day_product,
        'time_zone': time_zone,
        'store_id': store_id
    }

    monkeypatch.setattr(
        validators, 'validate_timed_release_dataset',
        MagicMock(return_value=response.Response(message=request_body)))

    result = product_live_time.create_product_live_time_details(
        product_id, time_of_day_product, time_zone, store_id)

    assert result.status == http_status.BAD_REQUEST


@patch(
    'timed_release.connectors.sql.db_session', side_effect=SQLAlchemyError())
def test_create_product_live_time_details_internal_error(monkeypatch):
    """Test create_product_live_time_details with SQLAlchemyError."""
    product_id = 2080166
    time_of_day_product = '20:30:00'
    time_zone = 'GMT'
    store_id = 286

    # mocking validators validate_time method with result true
    monkeypatch.setattr(
        validators, 'validate_time',
        MagicMock(return_value=response.Response(message=True)))

    insert_response = product_live_time.create_product_live_time_details(
        product_id, time_of_day_product, time_zone, store_id)

    assert insert_response.status == http_status.INTERNAL_ERROR


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
    expected_data = {
        'product_id': 12,
        'time_of_day_product': '20:30:00',
        'time_zone': 'GMT',
        'store_id': 1
    }
    db.insert_product_live_time_data()
    response = product_live_time.get_product_live_time_details('12')
    assert response.message == expected_data


@db.test_schema
def test_get_product_live_time_details_success_not_found():
    """Test that an existing product id is not found."""
    response = product_live_time.get_product_live_time_details('12')
    assert response.status == http_status.NOT_FOUND


@db.test_schema
def test_update_product_live_time_details_success():
    """Test to update product live time by product id."""
    db.insert_product_live_time_data()
    update_data = {
        'time_of_day_product': datetime.time(10, 20, 30),
        'time_zone': 'GMT',
        'store_id': 1
    }
    response = product_live_time.update_product_live_time_details(
        12, update_data)
    assert response.message == success.UPDATE_SUCCESS_MESSAGE.format(12)


@db.test_schema
def test_update_product_live_time_details_not_found():
    """Test to update product live time where product id not found."""
    update_data = {
        'time_of_day_product': datetime.time(10, 20, 30),
        'time_zone': 'GMT',
        'store_id': 1
    }
    response = product_live_time.update_product_live_time_details(
        11, update_data)
    assert response.status == http_status.NOT_FOUND


@db.test_schema
@patch(
    'timed_release.connectors.sql.db_session', side_effect=SQLAlchemyError())
def test_update_product_live_time_details_internal_error(monkeypatch):
    """Test to update product live time with SQLAlchemyError."""
    update_data = {
        'time_of_day_product': datetime.time(10, 20, 30),
        'time_zone': 'GMT',
        'store_id': 1
    }

    db.insert_product_live_time_data()
    response = product_live_time.update_product_live_time_details(
        11, update_data)

    assert response.status == http_status.INTERNAL_ERROR
