from __future__ import annotations

import datetime

import pymongo

from pymongo import IndexModel

from easy_logs.db import current_mongo

COLLECTION_PYTHON_HTTP_HANDLER = "python-http-handler"
COLLECTION_PYTHON_LUMBERJACK_HANDLER = "python-lumberjack-handler"


def _insert_log_(d: dict, collection: str):
    current_mongo[collection].insert_one(d)

def insert_python_lumberjack_handler(
        d: dict
):
    d["levelno"] = 0
    d["created"] = datetime.datetime.now()

    _insert_log_(d, COLLECTION_PYTHON_LUMBERJACK_HANDLER)

def insert_python_http_handler(
        d: dict
):
    d["levelno"] = int(d["levelno"])
    d["created"] = datetime.datetime.fromtimestamp(float(d["created"]))

    _insert_log_(d, COLLECTION_PYTHON_HTTP_HANDLER)


# ------------------------------------------------------------------------------------------------------------------
# Python
# ------------------------------------------------------------------------------------------------------------------

## Python HTTP handler
def make_indexes_python_http_handler():
    current_mongo[COLLECTION_PYTHON_HTTP_HANDLER].create_indexes([
        IndexModel([("levelname", pymongo.DESCENDING)]),
        IndexModel([("levelno", pymongo.DESCENDING)]),
        IndexModel([("created", pymongo.DESCENDING)]),
        IndexModel([("msg", pymongo.TEXT)])
    ])
