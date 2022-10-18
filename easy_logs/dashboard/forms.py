from flask_wtf import FlaskForm

from wtforms import StringField, validators, SelectField, IntegerField

class SearchForm(FlaskForm):
    log_level = SelectField(
        'Log Level',
        default='',
        choices=[
            ('', 'All Levels'),
            ('DEBUG', 'DEBUG'),
            ('INFO', 'INFO'),
            ('WARNING', 'WARNING'),
            ('ERROR', 'ERROR'),
            ('CRITICAL', 'CRITICAL')
        ],
        render_kw={"placeholder": "Log Level..."}
    )
    search_text = StringField('Search Text', default='', validators=[validators.Length(min=0, max=100)], render_kw={"placeholder": "Search Text... (press enter to search)"})
    page = IntegerField('Page', default=1, validators=[validators.NumberRange(min=1, max=1000)], render_kw={"placeholder": "Page..."})
