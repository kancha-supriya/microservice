"""Tests for the Sentry Connector."""

from unittest.mock import patch

from oto import response

from timed_release.connectors import sentry


@patch('timed_release.connectors.sentry.raven.Client',
       return_value='sentry_client')
@patch('timed_release.connectors.sentry.config')
def test_sentry_enabled(mock_config, mock_raven_client):
    """Test sentry.sentry_client is setup when config.SENTRY is set."""
    mock_config.SENTRY = 'SENTRY'
    sentry_client = sentry.get_client()
    assert sentry.sentry_client
    mock_raven_client.assert_called_with('SENTRY')
    assert sentry_client == 'sentry_client'


@patch('raven.Client', return_value='sentry_client')
@patch('timed_release.connectors.sentry.config')
def test_sentry_disabled(mock_config, mock_raven_client):
    """Test sentry.sentry_client initialized with dsn of None."""
    mock_config.SENTRY = None
    sentry_client = sentry.get_client()
    # last call is None
    mock_raven_client.assert_called_with(None)
    # sentry_client is returned
    assert sentry_client == 'sentry_client'


@patch('timed_release.connectors.sentry.sentry_client')
def test_send_response_to_sentry(mock_sentry_client):
    """Test sending an error message to Sentry."""
    error_response = response.Response(
        message='response message',
        errors={'error_code': 'error_message'},
        status=204)
    sentry_message = 'sentry message'

    # when sentry client exists, sentry message is sent
    mock_sentry_client.__bool__.return_value = True
    sentry.send_response_to_sentry(error_response, sentry_message)
    mock_sentry_client.captureMessage.assert_called_with(
        message=sentry_message,
        stack=True,
        extra={
            'message': error_response.message,
            'errors': error_response.errors,
            'status': error_response.status})
