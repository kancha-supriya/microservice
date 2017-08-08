"""Validations for logic."""

import datetime

from timed_release import config


def validate_time(time):
    """Validate given time in HH:MM:SS format.

    Args:
        time (str): time to validate
    Returns:
        return boolean true if valid time match with time format else false
    """
    try:
        datetime.datetime.strptime(time, config.DEFAULT_TIME_FORMAT)
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
