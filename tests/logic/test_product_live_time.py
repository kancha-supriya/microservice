"""Unit tests for ProductLiveTime logic."""

from unittest.mock import MagicMock
from oto import response
from oto import status as http_status

import pytest

from tests.testutils import db
from timed_release.constants import error
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
