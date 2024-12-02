import os

import redis
from flask import current_app
from werkzeug.security import check_password_hash

from errors.errors import HTTPError

redis_host = os.getenv('REDIS_HOST')
redis_port = 6379
r = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)


def is_rate_limited(prefix, username):
    attempts_key = f"login_attempts:{prefix}_{username}"
    attempts = r.get(attempts_key)
    conf = current_app.config["login"]

    if attempts:
        attempts = int(attempts)
        if attempts >= conf["max_attempts"]:
            raise HTTPError(429, "Too many login attempts. Please try again later.")

    r.incr(attempts_key)
    r.expire(attempts_key, conf["time_window"])
    return False


def check_credentials(prefix, username, db_password, password):
    if is_rate_limited(prefix, username):
        return False
    return check_password_hash(db_password, password)
