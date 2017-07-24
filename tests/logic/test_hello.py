"""Test for the Hello Handler."""

import pytest

from app_name.logic import hello


@pytest.mark.parametrize('name', [
    None, '', ' '])
def test_hello_without_valid_name(name):
    """Test saying hello without providing a name."""
    assert hello.say_hello(name).message == 'Hello'


def test_hello_with_name():
    """Test saying hello with a name."""
    assert hello.say_hello('Jess').message == 'Hello Jess!'
