from flask import Flask, jsonify

from errors.errors import HTTPError, HTTPInternalServerError


def handle_generic_error(e):
    response = {
        "error": "service_unavailable",
        "error_description": "Service Unavailable"
    }
    return jsonify(response), 500


def handle_http_error(e: HTTPError):
    return e.get_response()


def register_errors(app: Flask):
    app.register_error_handler(HTTPError, handle_http_error)
    app.register_error_handler(Exception, handle_generic_error)
