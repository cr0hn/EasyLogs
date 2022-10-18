from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class UserLogin(FlaskForm):
    name = StringField('name', validators=[DataRequired()], render_kw={"placeholder": "Enter user name..."})
    password = PasswordField('password', validators=[DataRequired()], render_kw={"placeholder": "Enter user password..."})

__all__ = ("UserLogin",)
