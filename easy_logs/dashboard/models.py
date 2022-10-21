from __future__ import annotations

import datetime
from typing import Tuple, List

import pymongo

from pymongo import IndexModel

from easy_logs.db import current_mongo

COLLECTION_PYTHON_HTTP_HANDLER = "python-http-handler"
MAX_TOTAL_LOGS = 500

def get_loggers_names() -> List[Tuple[str, str]]:
    return [
        *[('', 'All Loggers')],
        *[
            (logger_name, logger_name.capitalize())
            for logger_name in current_mongo[COLLECTION_PYTHON_HTTP_HANDLER].distinct("name")
        ]
    ]

def get_python_handler_logs(
        filter_date_order: str = None,
        filter_log_level: str = None,
        filter_search_text: str = None,
        filter_logger_name: str = None,
        page: int = 1,
        max_per_page: int = 50
) -> Tuple[int, list[dict]]:
    """
    Returns the logs from the python http handler as format:

    (total, logs)
    """

    if filter_date_order:
        if filter_date_order == "desc":
            date_order = pymongo.DESCENDING
        else:
            date_order = pymongo.ASCENDING
    else:
        date_order = pymongo.DESCENDING

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

    filter_steps = []

    if filter_search_text is not None:
        filter_steps.append({
            "$text": {
                "$search": filter_search_text
            }
        })

    if filter_log_level:
        filter_steps.append({
            "levelno": {
                "$gte": filter_log_level
            }
        })

    if filter_logger_name:
        filter_steps.append({
            "name": filter_logger_name
        })

    if filter_steps:

        if len(filter_steps) > 0:
            filters = {
                "$and": filter_steps
            }
        else:
            filters = filter_steps[0]

    else:
        filters = {}

    total = current_mongo[COLLECTION_PYTHON_HTTP_HANDLER].count_documents(filters)

    # We only get 500 logs at a time
    if total > MAX_TOTAL_LOGS:
        total = MAX_TOTAL_LOGS

    docs = list(current_mongo[COLLECTION_PYTHON_HTTP_HANDLER].find(
        filters
    ).sort("created", date_order).skip(
        (page - 1) * max_per_page
    ).limit(max_per_page))

    return total, docs
