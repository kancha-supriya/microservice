"""Validations for timed release module."""

import datetime

from timed_release import config
from timed_release.constants import error


def validate_time(time_value):
    """Validate given time in HH:MM:SS format.

    Args:
        time_value (str): time to validate
    Returns:
        return boolean true if valid time match with time format else false
    """
    try:
        datetime.datetime.strptime(time_value, config.DEFAULT_TIME_FORMAT)
        return True
    except ValueError:
        return False


def is_integer_and_non_negative(value):
    """Validate given value is integer and can not be negative.

    Args:
        value: value to check integer and can not be negative
    Returns:
        return boolean true if value is integer and greater than zero else
        false
    """
    if not isinstance(value, int) or value <= 0:
        return False
    return True


def mandatory_fields(data, mandatory_fields_list):
    """Validate mandatory fields.

    Args:
        data (dict): dict of data
        mandatory_fields_list (list): list of required fields
    Returns:
        return dict of fields those are not present in data
    """
    # checking fields in mandatory_fields_list is present in data if not
    # then return the dict of those fields.
    return [field for field in mandatory_fields_list if field not in data]


def validate_time_zone(time_zone):
    """Validate time zone.

    Args:
        time_zone (str): time zone
    Returns:
        return boolean true if valid time zone match with TIME_ZONES else
        false
    """
    if time_zone in config.TIME_ZONES:
        return True
    return False


def validate_timed_release_dataset(data, required_fields):
    """Validate an incoming dataset.

    Args:
        data (dict): the dataset to validate.
        required_fields (list): list of required fields.
    Returns:
        Response: with the result of the operation and a clean dataset.
    """
    validation_errors = []
    integer_and_non_negative_check_fields = ['product_id', 'store_id']

    # check for mandatory_fields
    mandatory_fields_validation = mandatory_fields(data, required_fields)
    if mandatory_fields_validation:
        field = {'missing mandatory fields': mandatory_fields_validation}
        validation_errors.append(field)

    # check for product_id and store_id is integer and
    # greater than zero
    integer_and_non_negative = [
        field for field in integer_and_non_negative_check_fields
        if data.get(field) and not is_integer_and_non_negative(data[field])]

    if integer_and_non_negative:
        fields = {
            'non integer or negative fields list': integer_and_non_negative}
        validation_errors.append(fields)

    # validate time_of_day_product
    if data.get('time_of_day_product') and \
            not validate_time(data['time_of_day_product']):
        field = {'invalid time zone': error.ERROR_MESSAGE_TIME_OF_DAY_RELEASE}
        validation_errors.append(field)

    # check time zone is local or GMT
    if data.get('time_zone') and not validate_time_zone(data['time_zone']):
        field = {'invalid time format': error.ERROR_MESSAGE_TIME_ZONE}
        validation_errors.append(field)

    return validation_errors
