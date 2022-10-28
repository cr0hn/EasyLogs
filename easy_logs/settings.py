from __future__ import annotations

import secrets

from sanic_envconfig import EnvConfig

class EasyLogsConfig(EnvConfig):
    DEBUG: bool = True
    # SERVER_NAME: str = "localhost:5000"

    SECRET_KEY: str = "aslñkjoaihs9y198y8o7Guyasbhucbzhuasdf_Z:mañpsdjoi1"

    MONGO_DB: str = "easylogs"
    MONGO_URI: str = "mongodb://root:example@127.0.0.1:27099"

    ADMIN_USER: str = "admin"
    ADMIN_PASSWORD: str = "adminadmin"

    RECEIVE_LOGS_KEY: str = "LIh982y87GgljahsadfklJHLIUG87g1u1e7f6eb2ee145571858e8e24"

    FLASK_PYDANTIC_VALIDATION_ERROR_RAISE: bool = True

    SESSION_TYPE: str = "redis"
    SESSION_KEY_PREFIX: str = "easylogs:session:"
    SESSION_COOKIE_NAME: str = "easylogs_session"
    REDIS_URI: str = "redis://127.0.0.1:6379/0"

__all__ = ("EasyLogsConfig",)
