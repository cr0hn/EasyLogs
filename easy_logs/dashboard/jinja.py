import re

import orjson

from flask import Flask

from .models import MAX_TOTAL_LOGS

REGEX_PAGE = re.compile(r"page=\d+")

def setup_jinja_dashboard(_app: Flask):

    @_app.template_filter("log_level_color")
    def log_level_color(log_level: str):
        if log_level == "DEBUG":
            return "text-info"
        elif log_level == "INFO":
            return "text-success"
        elif log_level == "WARNING":
            return "text-warning"
        elif log_level == "ERROR":
            return "text-danger"
        elif log_level == "CRITICAL":
            return "text-danger"
        else:
            return "text-dark"

    def add_page(url: str, page: int):
        # Ad or replace page in url
        if url.find("?") == -1:
            return f"{url}?page={page}"

        else:
            if url.find("page=") == -1:
                return f"{url}&page={page}"
            else:
                return REGEX_PAGE.sub(f"page={page}", url)
    def change_url_order(url: str):
        if "date_order=desc" in url:
            new_order = "asc"
            current_order = "desc"
        else:
            new_order = "desc"
            current_order = "asc"

        if "date_order=" in url:
            return url.replace(f"date_order={current_order}", f"date_order={new_order}")

        else:
            # Ad or replace page in url
            if "?" not in url:
                return f"{url}?date_order={new_order}"

            else:
                return f"{url}&date_order={new_order}"

    @_app.template_filter("pretty_print_json")
    def pretty_print_json(value):
        if type(value) is str:
            v = orjson.loads(value)
        else:
            v = value

        if "_id" in v:
            del v["_id"]

        return orjson.dumps(v, option=orjson.OPT_INDENT_2).decode()

    _app.jinja_env.globals.update(add_page=add_page)
    _app.jinja_env.globals.update(change_url_order=change_url_order)
    _app.jinja_env.globals.update(MAX_TOTAL_LOGS=MAX_TOTAL_LOGS)
