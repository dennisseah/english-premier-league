""" http helper functions """
from flask import make_response


def json_response(obj: object) -> object:
    resp = make_response(obj)
    resp.mimetype = "application/json"
    return resp


def bad_req_response(body: str) -> object:
    return make_response(body, 400)


def not_found_req_response(body: str) -> object:
    return make_response(body, 404)
