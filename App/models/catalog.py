from ..extensions import db


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(32), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    total_copies = db.Column(db.Integer, nullable=False, default=0)
    available_copies = db.Column(db.Integer, nullable=False, default=0)

    category = db.relationship("Category")
    authors = db.relationship("Author", secondary="book_authors", lazy="joined")
    copies = db.relationship("BookCopy", backref="book", cascade="all, delete-orphan")


class BookAuthor(db.Model):
    __tablename__ = "book_authors"
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), primary_key=True)


class BookCopy(db.Model):
    __tablename__ = "book_copies"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    barcode = db.Column(db.String(64), unique=True, nullable=False)
    status = db.Column(db.Enum("available", "issued", "lost", "repair", name="copy_status"), nullable=False, default="available")
