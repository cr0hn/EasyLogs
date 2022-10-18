from flask import Flask

from .bp_dashboard import bp_dashboard
from .jinja import setup_jinja_dashboard

def setup_dashboard(_app: Flask, api_prefix :str = None):
    _app.register_blueprint(bp_dashboard)

    setup_jinja_dashboard(_app)
