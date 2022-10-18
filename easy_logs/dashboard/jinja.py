import re

from flask import Flask

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

    _app.jinja_env.globals.update(add_page=add_page)
