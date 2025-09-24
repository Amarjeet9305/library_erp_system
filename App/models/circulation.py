from datetime import date
from ..extensions import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    copy_id = db.Column(db.Integer, db.ForeignKey("book_copies.id"), nullable=False)

    issue_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    fine_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    status = db.Column(db.Enum("issued", "returned", "overdue", name="tx_status"), nullable=False, default="issued")

    user = db.relationship("User")
    book = db.relationship("Book")
    copy = db.relationship("BookCopy")
