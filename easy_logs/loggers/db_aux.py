from flask import current_app

from easy_logs.db import current_mongo

def insert_log(data: dict, collection: str):
    current_mongo[collection].insert_one(data)


__all__ = ("insert_log",)
