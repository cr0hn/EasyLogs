from flask_paginate import Pagination
from flask_login import login_required
from flask import Blueprint, render_template, request

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

    pagination = Pagination(page=form.page.data, total=total, per_page=MAX_PER_PAGE)


    return render_template(
        "dashboard/home.html",
        pagination=pagination,
        form=form,
        logs_total_pages=total_pages,
        logs_per_page=MAX_PER_PAGE,
        logs=logs,
        log_source="python-http-handler"
    )
