from __future__ import annotations

import datetime
from typing import Tuple

import pymongo

from pymongo import IndexModel

from easy_logs.db import current_mongo

COLLECTION_PYTHON_HTTP_HANDLER = "python-http-handler"

def get_python_handler_logs(
        filter_log_level: str = None,
        filter_search_text: str = None,
        page: int = 1,
        max_per_page: int = 50
) -> Tuple[int, list[dict]]:

    if filter_log_level:
        # Map log level name to log number
        FILTER_LOG_LEVELS = {
            "DEBUG": 10,
            "INFO": 20,
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL": 50
        }

        try:
            filter_log_level = FILTER_LOG_LEVELS[filter_log_level]
        except KeyError:
            filter_log_level = 0

    else:
        filter_log_level = 0

    if not filter_search_text:
        filter_search_text = None

    filters = {}

    if filter_log_level is None and filter_search_text is not None:
        filters = {
            "$text": {
                "$search": filter_search_text
            }
        }

    elif filter_log_level is not None and filter_search_text is None:
        filters = {
            "levelno": {"$gte": filter_log_level}
        }

    elif filter_log_level is not None and filter_search_text is not None:
        filters = {
            "$and": [
                {
                    "$text": {
                        "$search": filter_search_text
                    }
                },
                {
                    "levelno": {"$gte": filter_log_level}
                }
            ]
        }

    total = current_mongo[COLLECTION_PYTHON_HTTP_HANDLER].count_documents(filters)
    docs = list(current_mongo[COLLECTION_PYTHON_HTTP_HANDLER].find(
        filters
    ).sort("created", pymongo.DESCENDING).skip(
        (page - 1) * max_per_page
    ).limit(max_per_page))

    return total, docs
