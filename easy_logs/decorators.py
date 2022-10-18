from functools import wraps
from typing import Callable

from flask import request, current_app, abort

from .exceptions import EasyLogsAuthenticationException

def ensure_auth(func):

    @wraps(func)
    def decorated(*args, **kwargs):
        config_key = current_app.config.get("RECEIVE_LOGS_KEY", None)
        webhook_key = request.args.get("key", None)

        if not webhook_key:
            raise EasyLogsAuthenticationException()

        if config_key != webhook_key:
            raise EasyLogsAuthenticationException()

        return func(*args, **kwargs)

    return decorated

__all__ = ("ensure_auth",)
