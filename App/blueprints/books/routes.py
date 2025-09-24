from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from ...extensions import db
from ...models import Book, Category, Author, BookAuthor
from .forms import BookForm


books_bp = Blueprint("books", __name__)


@books_bp.route("/")
@login_required
def list_books():
    q = request.args.get("q", "").strip()
    query = Book.query
    if q:
        like = f"%{q}%"
        query = query.filter((Book.title.ilike(like)) | (Book.isbn.ilike(like)))
    books = query.order_by(Book.title.asc()).all()
    return render_template("books/list.html", books=books, q=q)


@books_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_book():
    form = BookForm()
    if form.validate_on_submit():
        category = None
        if form.category.data:
            category = Category.query.filter_by(name=form.category.data.strip()).first()
            if not category:
                category = Category(name=form.category.data.strip())
                db.session.add(category)
        book = Book(
            isbn=form.isbn.data.strip(),
            title=form.title.data.strip(),
            category=category,
            total_copies=form.total_copies.data or 1,
            available_copies=form.total_copies.data or 1,
        )
        db.session.add(book)
        db.session.flush()
        if form.authors.data:
            names = [a.strip() for a in form.authors.data.split(",") if a.strip()]
            for name in names:
                author = Author.query.filter_by(full_name=name).first()
                if not author:
                    author = Author(full_name=name)
                    db.session.add(author)
                    db.session.flush()
                db.session.add(BookAuthor(book_id=book.id, author_id=author.id))
        db.session.commit()
        flash("Book created", "success")
        return redirect(url_for("books.list_books"))
    return render_template("books/form.html", form=form)


@books_bp.route("/<int:book_id>/edit", methods=["GET", "POST"])
@login_required
def edit_book(book_id: int):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    if request.method == "GET":
        form.category.data = book.category.name if book.category else ""
        form.authors.data = ", ".join(a.full_name for a in book.authors)
    if form.validate_on_submit():
        book.isbn = form.isbn.data.strip()
        book.title = form.title.data.strip()
        if form.category.data:
            category = Category.query.filter_by(name=form.category.data.strip()).first()
            if not category:
                category = Category(name=form.category.data.strip())
                db.session.add(category)
            book.category = category
        else:
            book.category = None
        book.total_copies = form.total_copies.data or book.total_copies
        if book.available_copies > book.total_copies:
            book.available_copies = book.total_copies
        # update authors
        db.session.query(BookAuthor).filter_by(book_id=book.id).delete()
        if form.authors.data:
            names = [a.strip() for a in form.authors.data.split(",") if a.strip()]
            for name in names:
                author = Author.query.filter_by(full_name=name).first()
                if not author:
                    author = Author(full_name=name)
                    db.session.add(author)
                    db.session.flush()
                db.session.add(BookAuthor(book_id=book.id, author_id=author.id))
        db.session.commit()
        flash("Book updated", "success")
        return redirect(url_for("books.list_books"))
    return render_template("books/form.html", form=form)


@books_bp.route("/<int:book_id>/delete", methods=["POST"])
@login_required
def delete_book(book_id: int):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash("Book deleted", "info")
    return redirect(url_for("books.list_books"))
