"""Validations for Model."""


def check_for_digit_and_non_zero(value):
    """Check if the value is digit and greater than zero.

    Args:
        value (str)

    Returns:
        return boolean true if value is integer and greater than zero else
        false.
    """
    if not value.isdigit() or int(value) <= 0:
        return False
    return True
