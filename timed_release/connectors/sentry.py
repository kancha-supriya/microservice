"""Sentry Client.

Provides sentry_client attribute for ad hoc capturing of messages and errors.

https://docs.getsentry.com/hosted/clients/python/usage/
"""

import raven

from timed_release import config


def get_client():
    """Return initialized Sentry client.

    If config.SENTRY is set, an initialized Sentry client is returned, if
    it is not set, a Client initialized with None is returned but nothing
    will be sent to Sentry.

    Returns:
        raven.Client: Sentry client that to capture messages and error.
    """
    sentry_client = raven.Client(config.SENTRY)
    return sentry_client


def send_response_to_sentry(response, sentry_message):
    """Send a Response object to Sentry.

    This method should be used to send a Response object & message
    to Sentry when an error occurs that we should be alerted about.

    ex.
        error_response = response.create_fatal_response('Something bad')
        sentry.send_response_to_sentry(error_response, response.errors['code'])

    Args:
        response (Response): Response object to send to Sentry.
        sentry_message (str): Message to be displayed in Sentry. Best practice
            for errors is for the sentry_message to be the error code so that
            all errors of the same type are grouped together.
    """
    sentry_client.captureMessage(
        message=sentry_message,
        stack=True,
        extra={
            'message': response.message,
            'errors': response.errors,
            'status': response.status})


sentry_client = get_client()
