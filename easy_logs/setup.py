import redis
import flask_pydantic

from flask_sse import sse
from flask_cors import CORS
from flask_session import Session
from flask import Flask, render_template

from .auth import setup_auth
from .loggers import setup_logs
from .cli import setup_global_cli
from .dashboard import setup_dashboard
from .healt_check import setup_health_check
from .exceptions import EasyLogsAuthenticationException

API_PREFIX = "/loggers"

def setup_errors(_app: Flask):

    @_app.errorhandler(flask_pydantic.exceptions.ValidationError)
    def handle_validations(e):
        return str(e), 400

    @_app.errorhandler(EasyLogsAuthenticationException)
    def handle_easylogs_auth(e):
        return str(e), 403

    @_app.errorhandler(500)
    def handle_500(e):
        return render_template("errors/500.html")

    # @_app.errorhandler(403)
    # @_app.errorhandler(401)
    @_app.errorhandler(404)
    def handle_404(e):
        return render_template("errors/40x.html"), 404

def setup_sessions(_app: Flask):

    # If we're in development mode, we don't want to use redis
    _app.config["SESSION_REDIS"] = redis.Redis.from_url(_app.config["REDIS_URI"])

    Session(_app)

def setup_sse(_app: Flask):
    _app.config["REDIS_URL"] = _app.config["REDIS_URI"]
    _app.register_blueprint(sse, url_prefix='/stream')

def setup_cors(_app: Flask):
    CORS(_app, resources={r"/*": {"origins": "*"}})

def setup_app() -> Flask:

    app = Flask(__name__)
    app.config.from_object("easy_logs.settings.EasyLogsConfig")

    setup_sse(app)
    setup_cors(app)
    setup_errors(app)
    setup_sessions(app)
    setup_global_cli(app)

    # -------------------------------------------------------------------------
    # Blueprints
    # -------------------------------------------------------------------------
    setup_logs(app, API_PREFIX)
    setup_auth(app, API_PREFIX)
    setup_dashboard(app, API_PREFIX)
    setup_health_check(app, API_PREFIX)

    return app
