from flask import jsonify


class HTTPError(Exception):
    default_error_description = ""
    default_error_code = ""

    def __init__(self, http_code, error_description=None, error_code=None):
        self.http_code = http_code
        self.error_code = error_code
        self.error_description = error_description

    def get_response(self):
        response = {
            "error": self.error_code or self.default_error_code,
            "error_description": self.error_description or self.default_error_description
        }
        return jsonify(response), self.http_code

    @staticmethod
    def raise_error_from_response(response):
        raise HTTPError(
            response.status_code,
            error_description=response.json()["error_description"],
            error_code=response.json()["error"],
        )


class HTTPBadRequestError(HTTPError):
    http_code = 400
    default_error_code = "bad_request"

    def __init__(self, error_description=None, error_code=None):
        super().__init__(self.http_code, error_description, error_code)


class HTTPUnauthorizedError(HTTPError):
    http_code = 401
    default_error_code = "unauthorized"

    def __init__(self, error_description=None, error_code=None):
        super().__init__(self.http_code, error_description, error_code)


class HTTPForbiddenError(HTTPError):
    http_code = 403
    default_error_code = "forbidden"

    def __init__(self, error_description=None, error_code=None):
        super().__init__(self.http_code, error_description, error_code)


class HTTPNotFoundError(HTTPError):
    http_code = 404
    default_error_code = "not_found"

    def __init__(self, error_description=None, error_code=None):
        super().__init__(self.http_code, error_description, error_code)


class HTTPInternalServerError(HTTPError):
    http_code = 500
    default_error_code = "internal_server_error"
    default_message = "An error occurred while processing your request"

    def __init__(self, error_description=None, error_code=None):
        super().__init__(self.http_code, error_description, error_code)
