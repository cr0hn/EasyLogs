import pymongo

from pymongo.database import Database, Collection as MongoCollection

from werkzeug.local import LocalProxy
from flask import g, current_app, Flask


# -------------------------------------------------------------------------
# Setup Mongo
# -------------------------------------------------------------------------
def make_mongo_connection(_app: Flask):
    client = pymongo.MongoClient(_app.config['MONGO_URI'])
    db = client[_app.config['MONGO_DB']]
    return db, client

def _get_mongo_connection():
    if 'mongo_database' not in g:
        g.mongo_database, g.mongo_client = make_mongo_connection(current_app)

    return g.mongo_database


current_mongo: Database = LocalProxy(_get_mongo_connection)


__all__ = ("current_mongo", "MongoCollection")

