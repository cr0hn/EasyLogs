from flask import Flask

from .python import bp_python_http_handler

def setup_logs(_app: Flask, api_prefix:str = None):
    _app.register_blueprint(bp_python_http_handler, url_prefix=api_prefix)
