from urllib.parse import urlparse, urljoin

from flask import Blueprint, render_template, request, flash, url_for, redirect, current_app, abort
from flask_login import logout_user, login_user, login_required

from .forms import *
from .models import *

bp_auth = Blueprint(
    name="bp_auth",
    import_name=__name__,
    template_folder="templates"
)

@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLogin(request.form)

    if form.validate_on_submit():
        if current_app.config["ADMIN_USER"] == form.name.data and current_app.config["ADMIN_PASSWORD"] == form.password.data:
            login_user(User(name=current_app.config["ADMIN_USER"]))

            return redirect(url_for('bp_dashboard.home'))

        else:
            flash("User or password incorrect", "error")

            return render_template('login/login.html', form=form)

    else:
        return render_template("login/login.html", form=form, method="GET")



@bp_auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('bp_auth.login'))
