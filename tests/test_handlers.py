"""Tests for Handlers."""

import json
from unittest.mock import MagicMock
from unittest.mock import patch

from oto import response

from app_name import handlers


@patch('app_name.handlers.g')
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
