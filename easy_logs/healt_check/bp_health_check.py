from flask import Blueprint

bp_health_check = Blueprint(
    name="bp_health_check",
    import_name=__name__
)

@bp_health_check.route('/health-check', methods=['GET'])
def health_check():
    return "App is running!"
