"""Test for validators."""

import pytest

from timed_release.validation import validators


@pytest.mark.parametrize(
    'description, time, expected_response', [
        ('testing with valid time', '20:15:00', True),
        ('testing with invalid time', '85:00:00', False)])
def test_validate_time(description, time, expected_response):
    """Test for validate_time."""
    result = validators.validate_time(time)

    assert result == expected_response


@pytest.mark.parametrize(
    'description, value, expected_response', [
        ('testing with valid integer value', 2080166, True),
        ('testing with invalid integer value', -2080168, False)])
def test_is_integer_and_non_negative(description, value, expected_response):
    """Test for is_integer_and_non_negative."""
    result = validators.is_integer_and_non_negative(value)

    assert result == expected_response


@pytest.mark.parametrize(
    'description, time_zone, expected_response', [
        ('testing with valid time zone', 'GMT', True),
        ('testing with invalid time zone', 'UTC', False)])
def test_validate_time_zone(description, time_zone, expected_response):
    """Test for validate_time_zone."""
    result = validators.validate_time_zone(time_zone)

    assert result == expected_response


@pytest.mark.parametrize(
    'description, data, mandatory_fields_list, expected_response', [
        ('testing with product_id missing',
            {'time_of_day_product': '20:15:00', 'time_zone': 'local',
                'store_id': 286},
            ['product_id', 'time_of_day_product', 'time_zone'],
            ['product_id']),
        ('testing with empty request body', {},
            ['product_id', 'time_of_day_product', 'time_zone'],
            ['product_id', 'time_of_day_product', 'time_zone'])])
def test_mandatory_fields(
        description, data, mandatory_fields_list, expected_response):
    """Test for mandatory_fields."""
    result = validators.mandatory_fields(data, mandatory_fields_list)

    assert result == expected_response


@pytest.fixture
def validation_errors_response():
    """Get validation errors message.

    Returns:
        list: validation errors message
    """
    return [
        {
            'non integer or negative fields list': ['product_id', 'store_id']
        }, {
            'invalid time zone': 'Time of day Product should be in valid '
                                 'HH:MM:SS format'
        }, {
            'invalid time format': 'Time Zone should be GMT or local'
        }
    ]


@pytest.mark.parametrize(
    'description, data, mandatory_fields_list, expected_response', [
        ('testing with validation errors',
            {'product_id': -2080166, 'time_of_day_product': '85:15:00',
                'time_zone': 'UTC', 'store_id': -286},
            ['product_id', 'time_of_day_product', 'time_zone'],
            validation_errors_response()),
        ('testing with valid dataset',
            {'product_id': 2080166, 'time_of_day_product': '20:15:00',
                'time_zone': 'GMT', 'store_id': 286},
            ['product_id', 'time_of_day_product', 'time_zone'], [])])
def test_validate_timed_release_dataset(
        description, data, mandatory_fields_list, expected_response):
    """Test for validate_timed_release_dataset."""
    result = validators.validate_timed_release_dataset(
        data, mandatory_fields_list)

    assert result == expected_response
