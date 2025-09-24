from flask import Blueprint, render_template
from flask_login import login_required
from datetime import date, timedelta
from ...models import Transaction


reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/")
@login_required
def index():
    today = date.today()
    start_week = today - timedelta(days=today.weekday())
    start_month = today.replace(day=1)

    daily = Transaction.query.filter(Transaction.issue_date == today).count()
    weekly = Transaction.query.filter(Transaction.issue_date >= start_week).count()
    monthly = Transaction.query.filter(Transaction.issue_date >= start_month).count()

    return render_template("dashboard.html", stats={"daily": daily, "weekly": weekly, "monthly": monthly})
