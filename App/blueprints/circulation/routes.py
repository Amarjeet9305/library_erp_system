from decimal import Decimal
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from datetime import date
from ...extensions import db
from ...models import Book, BookCopy, Transaction
from ...utils.fines import calculate_overdue_fine
from .forms import IssueForm, ReturnForm


circ_bp = Blueprint("circulation", __name__)


@circ_bp.route("/issue", methods=["GET", "POST"])
@login_required
def issue_book():
    form = IssueForm()
    if form.validate_on_submit():
        book = Book.query.get_or_404(form.book_id.data)
        copy = BookCopy.query.get_or_404(form.copy_id.data)
        if copy.status != "available":
            flash("Copy not available", "danger")
            return render_template("circulation/issue.html", form=form)
        tx = Transaction(
            user_id=form.user_id.data,
            book_id=book.id,
            copy_id=copy.id,
            issue_date=form.issue_date.data,
            due_date=form.due_date.data,
            status="issued",
        )
        copy.status = "issued"
        if book.available_copies > 0:
            book.available_copies -= 1
        db.session.add(tx)
        db.session.commit()
        flash("Book issued", "success")
        return redirect(url_for("circulation.issue_book"))
    return render_template("circulation/issue.html", form=form)


@circ_bp.route("/return", methods=["GET", "POST"])
@login_required
def return_book():
    form = ReturnForm()
    if form.validate_on_submit():
        tx = Transaction.query.get_or_404(form.transaction_id.data)
        if tx.status == "returned":
            flash("Already returned", "info")
            return render_template("circulation/return.html", form=form)
        tx.return_date = form.return_date.data
        tx.status = "returned"
        fine = calculate_overdue_fine(tx.due_date, tx.return_date, Decimal("2.00"))
        tx.fine_amount = fine
        copy = tx.copy
        copy.status = "available"
        book = tx.book
        book.available_copies += 1
        db.session.commit()
        flash(f"Book returned. Fine: {fine}", "success")
        return redirect(url_for("circulation.return_book"))
    return render_template("circulation/return.html", form=form)
