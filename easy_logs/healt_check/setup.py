from flask import Flask

from .bp_health_check import bp_health_check

def setup_health_check(_app: Flask, api_prefix :str = None):
    _app.register_blueprint(bp_health_check)
