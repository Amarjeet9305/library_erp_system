from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length


class BookForm(FlaskForm):
    isbn = StringField("ISBN", validators=[DataRequired(), Length(max=32)])
    title = StringField("Title", validators=[DataRequired(), Length(max=255)])
    category = StringField("Category", validators=[Length(max=128)])
    authors = StringField("Authors (comma-separated)")
    total_copies = IntegerField("Total Copies", default=1)
    submit = SubmitField("Save")
