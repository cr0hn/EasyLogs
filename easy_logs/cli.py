from flask import Flask

from easy_logs.loggers.python.models import make_indexes_python_http_handler

def setup_global_cli(_app: Flask):

    @_app.cli.command("create-mongo-indexes")
    def create_mongo_indexes():

        with _app.app_context():
            make_indexes_python_http_handler()

__all__ = ("setup_global_cli",)
