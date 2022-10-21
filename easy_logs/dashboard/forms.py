from flask_wtf import FlaskForm

from wtforms import StringField, validators, SelectField, IntegerField

from .models import get_loggers_names

class SearchForm(FlaskForm):
    log_level = SelectField(
        'Log Level',
        default='',
        choices=[
            ('', 'All log levels'),
            ('DEBUG', '>= DEBUG'),
            ('INFO', '>= INFO'),
            ('WARNING', '>= WARNING'),
            ('ERROR', '>= ERROR'),
            ('CRITICAL', '>= CRITICAL')
        ],
        render_kw={"placeholder": "Log Level..."}
    )
    logger_name = SelectField(
        'Log Level',
        default='',
        choices=lambda: get_loggers_names(),
        render_kw={"placeholder": "Log name..."}
    )
    date_order = SelectField('Date Order', default='desc', choices=[('desc', 'desc'), ('asc', 'asc')])
    search_text = StringField('Search Text', default='', validators=[validators.Length(min=0, max=100)], render_kw={"placeholder": "Search Text... (press enter to search)"})
    page = IntegerField('Page', default=1, validators=[validators.NumberRange(min=1, max=1000)], render_kw={"placeholder": "Page..."})
