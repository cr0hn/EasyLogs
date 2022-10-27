from flask import Flask
from flask_login import LoginManager

from .models import User
from .bp_auth import bp_auth


def setup_login(_app: Flask):

    login_manager = LoginManager(_app)
    login_manager.login_view = 'bp_auth.login'
    login_manager.login_message = 'Please login for access to the platform'
    login_manager.login_message_category = 'error'

    @login_manager.user_loader
    def load_user(user_id):
        return User(name=user_id)

    @login_manager.request_loader
    def load_user_from_request(request):
        return None

def setup_auth(_app: Flask, api_prefix :str = None):
    setup_login(_app)

    _app.register_blueprint(bp_auth)


