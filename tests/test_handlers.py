"""Tests for Handlers."""

import json
from unittest.mock import MagicMock
from unittest.mock import patch

from oto import response
from oto import status as http_status
import pytest

from timed_release import handlers
from timed_release.api import app
from timed_release.constants import error
from timed_release.constants import success
from timed_release.logic import product_live_time


@patch('timed_release.handlers.g')
def test_exception_handler(mock_g):
    """Verify exception_Handler returns 500 status code and json payload."""
    message = (
        'The server encountered an internal error '
        'and was unable to complete your request.')
    mock_error = MagicMock()
    server_response = handlers.exception_handler(mock_error)
    mock_g.log.exception.assert_called_with(mock_error)

    # assert status code is 500
    assert server_response.status_code == 500

    # assert json payload
    response_message = json.loads(server_response.data.decode())
    assert response_message['message'] == message
    assert response_message['code'] == response.error.ERROR_CODE_INTERNAL_ERROR


@pytest.mark.parametrize(
    'description, product_id, status', [
        ('Product id must be greater than zero', '0', 400),
        ('Product id must be greater than zero', '-1', 400),
        ('Product id must be integer', 'abc', 400)])
def test_get_product_live_time_detail_for_failure(
        description, product_id, status):
    """Test for get product live time with invalid product id."""
    request_url = '/product/{product_id}'.format(product_id=product_id)
    result = app.test_client().get(request_url)
    assert result.status_code == status


def test_get_product_live_time_detail_success(monkeypatch):
    """Test get product live time with valid product id."""
    expected_response = {
        'product_id': 122,
        'time_of_day_product': '02:01:00',
        'time_zone': 'GMT',
        'store_id': 1}

    monkeypatch.setattr(
        product_live_time, 'get_product_live_time_details',
        MagicMock(return_value=response.Response(message=expected_response)))

    result = app.test_client().get('/product/122')
    message = json.loads(result.data.decode())

    assert result.status_code == http_status.OK
    assert message == expected_response


def test_get_product_live_time_detail_for_not_found(monkeypatch):
    """Test for get product live time with product_id not found."""
    product_id = 1
    expected_response = error.ERROR_MESSAGE_PRODUCT_NOT_FOUND.format(
        product_id)
    monkeypatch.setattr(
        product_live_time, 'get_product_live_time_details',
        MagicMock(return_value=response.create_not_found_response(
            message=expected_response)))

    request_url = '/product/{product_id}'.format(product_id=product_id)

    result = app.test_client().get(request_url)

    assert result.status_code == http_status.NOT_FOUND


def test_get_product_live_time_detail_for_db_failure(mocker):
    """Test db failure response."""
    mocker.patch.object(
        product_live_time, 'get_product_live_time_details',
        return_value=response.Response(status=500))

    result = app.test_client().get('/product/1')

    assert result.status_code == http_status.INTERNAL_ERROR


def test_create_product_live_time_detail_success(monkeypatch):
    """Test for Create product live time detail success."""
    request_body = {
        'product_id': 2080166,
        'time_of_day_product': '20:15:00',
        'time_zone': 'local',
        'store_id': 286}
    expected_response = {'product': request_body}

    monkeypatch.setattr(
        product_live_time, 'create_product_live_time_detail',
        MagicMock(return_value=response.Response(message=expected_response)))

    with app.test_client() as client:
        result = client.post(
            '/product', data=json.dumps(request_body),
            content_type='application/json')
        message = json.loads(result.data.decode())

        assert result.status_code == http_status.OK
        assert message == expected_response


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
def test_create_product_live_time_detail_failure(
        description, product_id, time_of_day_product, time_zone, store_id,
        expected_response, monkeypatch):
    """Test for create product live time detail with failure."""
    request_body = {
        'product_id': product_id,
        'time_of_day_product': time_of_day_product,
        'time_zone': time_zone,
        'store_id': store_id}

    monkeypatch.setattr(
        product_live_time, 'create_product_live_time_detail',
        MagicMock(return_value=response.create_error_response(
            code=error.ERROR_CODE_BAD_REQUEST, message=expected_response)))

    with app.test_client() as client:
        result = client.post(
            '/product', data=json.dumps(request_body),
            content_type='application/json')

        assert result.status_code == http_status.BAD_REQUEST


def test_create_product_live_time_detail_db_failure(mocker):
    """Test db failure response."""
    request_body = {
        'product_id': 2080166,
        'time_of_day_product': '20:15:00',
        'time_zone': 'local',
        'store_id': 286}

    mocker.patch.object(
        product_live_time, 'create_product_live_time_detail',
        return_value=response.Response(status=500))

    with app.test_client() as client:
        result = client.post(
            '/product', data=json.dumps(request_body),
            content_type='application/json')

        assert result.status_code == http_status.INTERNAL_ERROR


@pytest.mark.parametrize('description, request_body', [
    ('test with empty request body', ''),
    ('test with invalid data passed to request body', 'abc')])
def test_create_product_live_time_detail_invalid_request_body(
        description, request_body):
    """Test for create product live time detail invalid request body."""
    with app.test_client() as client:
        result = client.post('/product', data=request_body)

        assert result.status_code == http_status.BAD_REQUEST


def test_delete_product_live_details_success(monkeypatch):
    """Test delete product live time with success."""
    monkeypatch.setattr(
        product_live_time, 'delete_product_live_time_details',
        MagicMock(return_value=response.Response(
            message=success.DELETE_SUCCESS_MESSAGE_TIMED_RELEASE)))

    result = app.test_client().delete('/product/122')
    message = result.data.decode()

    assert result.status_code == http_status.OK
    assert message == success.DELETE_SUCCESS_MESSAGE_TIMED_RELEASE


def test_delete_product_live_details_for_not_found(monkeypatch):
    """Test for delete product live time with product_id not found."""
    product_id = 1
    expected_response = error.ERROR_MESSAGE_PRODUCT_NOT_FOUND.format(
        product_id)

    monkeypatch.setattr(
        product_live_time, 'delete_product_live_time_details',
        MagicMock(return_value=response.create_not_found_response(
            message=expected_response)))

    request_url = '/product/{product_id}'.format(product_id=product_id)
    result = app.test_client().delete(request_url)

    assert result.status_code == http_status.NOT_FOUND
