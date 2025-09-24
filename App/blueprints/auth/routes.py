from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from ...extensions import db
from ...models import User
from .forms import LoginForm, RegistrationForm


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        raw = form.identifier.data.strip()
        user = None
        if raw.isdigit():
            user = User.query.get(int(raw))
        else:
            user = User.query.filter_by(email=raw.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(request.args.get("next") or url_for("index"))
        flash("Invalid email/ID or password", "danger")
    elif request.method == "POST":
        flash("Please correct the errors below and try again.", "danger")
    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if existing:
            flash("Email already registered.", "danger")
            return render_template("register.html", form=form)
        user = User(
            email=form.email.data.lower().strip(),
            full_name=form.full_name.data.strip(),
            type="student",
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. You can now log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)
