from flask_pydantic import validate
from flask import Blueprint, request, jsonify, current_app

from easy_logs.decorators import ensure_auth

from .forms import PythonHTTPHandlerEntryLogForm
from .models import insert_python_http_handler

bp_python_http_handler = Blueprint(
    name="bp_python_http_handler",
    import_name=__name__
)

@bp_python_http_handler.route('/python/http-handler', methods=['POST'])
@ensure_auth
@validate(form=PythonHTTPHandlerEntryLogForm)
def push_logs():
    insert_python_http_handler(request.form.to_dict())

    return "OK", 200
