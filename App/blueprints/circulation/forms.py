from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired


class IssueForm(FlaskForm):
    user_id = IntegerField("User ID", validators=[DataRequired()])
    book_id = IntegerField("Book ID", validators=[DataRequired()])
    copy_id = IntegerField("Copy ID", validators=[DataRequired()])
    issue_date = DateField("Issue Date", validators=[DataRequired()])
    due_date = DateField("Due Date", validators=[DataRequired()])
    submit = SubmitField("Issue")


class ReturnForm(FlaskForm):
    transaction_id = IntegerField("Transaction ID", validators=[DataRequired()])
    return_date = DateField("Return Date", validators=[DataRequired()])
    submit = SubmitField("Return")
