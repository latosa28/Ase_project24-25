import re
from html import escape

from flask import request

from errors.errors import HTTPBadRequestError


def email_validation(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if not re.match(regex, email):
        raise HTTPBadRequestError("Invalid email format")


def get_body_field(key, mandatory=False, expected_type=str):
    value = request.json.get(key)

    if value:
        try:
            expected_type(value)
        except (ValueError, TypeError):
            raise HTTPBadRequestError(f"invalid {key} field format")
    else:
        if mandatory:
            raise HTTPBadRequestError(f"{key} field missing")
        return None

    return escape(value) if expected_type == str else value



