from flask import Blueprint, render_template, request
from flask_login import login_required

from .forms import SearchForm
from .models import get_python_handler_logs

MAX_PER_PAGE = 20

bp_dashboard = Blueprint(
    name="bp_dashboard",
    import_name=__name__,
    template_folder="templates"
)

@bp_dashboard.route('/', methods=['GET'])
@login_required
def home():

    form = SearchForm(request.args, meta={'csrf': False})

    if form.validate():
        total, logs = get_python_handler_logs(
            filter_log_level=form.log_level.data,
            filter_search_text=form.search_text.data,
            filter_logger_name=form.logger_name.data,
            filter_date_order=form.date_order.data,
            page=form.page.data,
            max_per_page=MAX_PER_PAGE
        )

    else:
        total, logs = get_python_handler_logs(
            page=form.page.data,
            max_per_page=MAX_PER_PAGE
        )

    # Calculate total pages
    total_pages = total // MAX_PER_PAGE

    if total_pages == 0:
        total_pages = 1

    # Calculate previous page
    previous_page = form.page.data - 1
    if previous_page < 1:
        previous_page = 1

    # Calculate next page
    next_page = form.page.data + 1
    if next_page > total_pages:
        next_page = total_pages

    return render_template(
        "dashboard/home.html",
        form=form,
        logs_page_step=3,
        logs_current_page=form.page.data,
        logs_previous_page=previous_page,
        logs_next_page=next_page,
        logs_total_pages=total_pages,
        logs_per_page=MAX_PER_PAGE,
        total_logs=total,
        logs=logs,
        log_source="python-http-handler"
    )
