import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
PIN_REGEX = re.compile(ur'^(\d{4}|\d{6})$')


def valid_email(email=None):
    if EMAIL_REGEX.match(email):
        return True
    else:
        return False


def validate_pin(pin=None):
    if re.match(PIN_REGEX, pin):
        return True
    else:
        return False
