from __future__ import annotations

import datetime

import pymongo

from pymongo import IndexModel

from easy_logs.db import current_mongo

COLLECTION_PYTHON_HTTP_HANDLER = "python-http-handler"

from ..db_aux import insert_log
from ..signals import signal_new_log_entry

def insert_python_http_handler(
        d: dict
):
    d["levelno"] = int(d["levelno"])
    d["created"] = datetime.datetime.fromtimestamp(float(d["created"]))

    insert_log(d, COLLECTION_PYTHON_HTTP_HANDLER)

    signal_new_log_entry(d["levelname"], d["msg"], d["name"], d["created"], d)

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
