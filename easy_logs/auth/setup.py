from flask import Flask, g, request
from flask_login import LoginManager, user_loaded_from_request

from .models import User
from .bp_auth import bp_auth


def setup_login(_app: Flask):

    login_manager = LoginManager(_app)
    login_manager.login_view = 'bp_auth.login'
    login_manager.login_message = 'Please login for access to the platform'
    login_manager.login_message_category = 'error'

    @user_loaded_from_request.connect
    def custom_user_loaded_from_request(app, user=None):
        g.login_via_request = True

    current_session_interface = _app.session_interface.save_session

    def custom_save_session(self, *args, **kwargs):
        if g.get('login_via_request') or request.path.startswith("/loggers"):
            return

        return current_session_interface(self, *args, **kwargs)

    _app.session_interface.save_session = custom_save_session

    @user_loaded_from_request.connect
    def custom_user_loaded_from_request(self, user=None):
        g.login_via_request = True

    @login_manager.user_loader
    def load_user(user_id):
        return User(name=user_id)

def setup_auth(_app: Flask, api_prefix :str = None):
    setup_login(_app)

    _app.register_blueprint(bp_auth)


