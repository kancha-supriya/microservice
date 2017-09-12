"""Unit tests for ProductLiveTime logic."""

from unittest.mock import MagicMock
from oto import response
from oto import status as http_status

import pytest

from tests.testutils import db
from timed_release.constants import error
from timed_release.constants import success
from timed_release.logic import product_live_time
from timed_release.models import product_live_time as product_live_time_model


@pytest.mark.parametrize(
    'description, product_id, status', [
        ('Product not found', '11', 404),
        ('Product id must be greater than zero', '0', 400),
        ('Product id must be greater than zero', '-1', 400),
        ('Product id must be integer', 'abc', 400)])
@db.test_schema
def test_get_product_live_time_detail_failure(description, product_id, status):
    """Test to get product live time for given product id."""
    response = product_live_time.get_product_live_time_details(product_id)
    assert response.status == status


def test_create_product_live_time_detail_success(monkeypatch):
    """Test for create product live time details with success."""
    request_body = {
        'product_id': 2080166,
        'time_of_day_product': '20:15:00',
        'time_zone': 'local',
        'store_id': 286}
    expected_response = {'product': request_body}

    monkeypatch.setattr(
        product_live_time_model, 'create_product_live_time_details',
        MagicMock(return_value=response.Response(message=expected_response)))

    result = product_live_time.create_product_live_time_detail(
        request_body)

    assert result.status == http_status.OK
    assert result.message == expected_response


@pytest.mark.parametrize(
    'description, product_id, time_of_day_product, time_zone, store_id, '
    'expected_response', [
        ('testing with product_id is non integer', '2080166xyz', '20:30:00',
            'GMT', 286,
            [{'non integer or negative fields list': ['product_id']}]),
        ('testing with invalid time', 2080169, '85:30:00', 'local', 286,
            [{'invalid time zone': 'Time of day Product should be in valid '
                'HH:MM:SS format'}]),
        ('testing with store_id has negative value', 2080168, '20:30:00',
            'GMT', -286,
            [{'non integer or negative fields list': ['store_id']}]),
        ('testing time zone with other than local or GMT', 2080170,
            '20:30:00', 'UTC', 286,
            [{'invalid time format': 'Time Zone should be GMT or local'}])])
def test_create_product_live_time_detail_validations(
        description, product_id, time_of_day_product, time_zone, store_id,
        expected_response, monkeypatch):
    """Test for create product live time details with validations."""
    request_body = {
        'product_id': product_id,
        'time_of_day_product': time_of_day_product,
        'time_zone': time_zone,
        'store_id': store_id}

    monkeypatch.setattr(
        product_live_time_model, 'create_product_live_time_details',
        MagicMock(return_value=response.create_error_response(
            code=error.ERROR_CODE_BAD_REQUEST, message=expected_response)))

    result = product_live_time.create_product_live_time_detail(
        request_body)

    assert result.status == http_status.BAD_REQUEST


@pytest.mark.parametrize(
    'description, request_body', [
        ('testing request body with product_id field missing',
            {'time_of_day_product': '20:15:00', 'time_zone': 'local',
                'store_id': 286}),
        ('testing request body with product_id,time_of_day_product,time_zone '
            'fields missing', {'store_id': 286}),
        ('testing with empty request body', {})])
def test_create_product_live_time_detail_mandatory_fields(
        description, request_body, monkeypatch):
    """Test for create product live time details with mandatory fields."""
    monkeypatch.setattr(
        product_live_time_model, 'create_product_live_time_details',
        MagicMock(return_value=response.create_error_response(
            code=error.ERROR_CODE_BAD_REQUEST, message=request_body)))

    result = product_live_time.create_product_live_time_detail(
        request_body)

    assert result.status == http_status.BAD_REQUEST


def test_delete_product_live_time_details_success(monkeypatch):
    """Test for delete product live time with success."""
    monkeypatch.setattr(
        product_live_time_model, 'delete_product_live_time_details',
        MagicMock(return_value=response.Response(
            message=success.DELETE_SUCCESS_MESSAGE_TIMED_RELEASE)))

    result = product_live_time.delete_product_live_time_details('12')

    assert result.status == http_status.OK
    assert result.message == success.DELETE_SUCCESS_MESSAGE_TIMED_RELEASE


@pytest.mark.parametrize(
    'description, product_id, expected_status', [
        ('Product id not found', '11', 404),
        ('Product id must be greater than zero', '0', 400),
        ('Product id must be greater than zero', '-1', 400),
        ('Product id must be integer', 'abc', 400)])
@db.test_schema
def test_delete_product_live_time_details_failure(
        description, product_id, expected_status):
    """Test for delete product live time with failure."""
    result = product_live_time.delete_product_live_time_details(product_id)
    assert result.status == expected_status


@pytest.mark.parametrize(
    'description, product_id, request_body', [
        ('Request body with time_of_day_product missing', '1',
            {'time_of_day_product': '', 'time_zone': 'local',
                'store_id': 286}),
        ('Invalid time', '1',
            {'time_of_day_product': '80:10:00', 'time_zone': 'local',
             'store_id': 286}),
        ('Store_id has negative value', '1',
            {'time_of_day_product': '80:10:00', 'time_zone': 'local',
             'store_id': -1}),
        ('Time Zone with other than local or GMT', '1',
            {'time_of_day_product': '80:10:00', 'time_zone': 'test',
             'store_id': 286}),
        ('Product id must be integer', 'abc',
            {'time_of_day_product': '80:10:00', 'time_zone': 'test',
             'store_id': 286}),
        ('Product id greater than zero', '-1',
            {'time_of_day_product': '80:10:00', 'time_zone': 'test',
             'store_id': 286}),
        ('Product id greater than zero', '0',
            {'time_of_day_product': '80:10:00', 'time_zone': 'test',
             'store_id': 286})])
def test_update_product_live_time_validation(
        description, product_id, request_body):
    """Test for update product live time details validation."""
    result = product_live_time.update_product_live_time(
        product_id, request_body)

    assert result.status == http_status.BAD_REQUEST


def test_update_product_live_time_success(monkeypatch):
    """Test for update product live time details."""
    expected_response = {
        'product':
            {
                'product_id': 11,
                'time_of_day_product': '03:02:01',
                'time_zone': 'GMT',
                'store_id': 1
            }}

    monkeypatch.setattr(
        product_live_time_model, 'update_product_live_time_details',
        MagicMock(return_value=response.Response(message=expected_response)))

    request_body = {
        'time_of_day_product': '03:02:01',
        'time_zone': 'GMT',
        'store_id': 1}

    result = product_live_time.update_product_live_time('11', request_body)

    assert result.status == http_status.OK
    assert result.message == expected_response


def test_update_product_live_time_for_product_not_found(monkeypatch):
    """Test for update product live time details when product id not found."""
    request_body = {
        'time_of_day_product': '03:02:01',
        'time_zone': 'GMT',
        'store_id': 1}

    monkeypatch.setattr(
        product_live_time_model, 'update_product_live_time_details',
        MagicMock(return_value=response.create_not_found_response(
            message=error.ERROR_MESSAGE_PRODUCT_NOT_FOUND.format(1)
        )))

    result = product_live_time.update_product_live_time('12', request_body)

    assert result.status == http_status.NOT_FOUND
