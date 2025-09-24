from flask import Blueprint, g, session, redirect, render_template, request, current_app
from Controllers.UserManager import UserManager
from Controllers.BookManager import BookManager

book_view = Blueprint('book_routes', __name__, template_folder='../templates')

def get_book_manager():
    return BookManager(current_app.config['DAO'])

def get_user_manager():
    return UserManager(current_app.config['DAO'])

@book_view.route('/books/', defaults={'id': None})
@book_view.route('/books/<int:id>')
def home(id):
    user_manager = get_user_manager()
    book_manager = get_book_manager()

    user_manager.user.set_session(session, g)

    if id:
        book = book_manager.getBook(id)
        if not book:
            return render_template("book_view.html", error="Book not found!")

        user_books = []
        if user_manager.user.isLoggedIn():
            reserved = book_manager.getReserverdBooksByUser(user_manager.user.uid())
            user_books = [b for b in reserved['user_books'].split(',') if b]

        return render_template("book_view.html", books=book, user_books=user_books, g=g)

    # List all books
    books = book_manager.list()
    user_books = []
    if user_manager.user.isLoggedIn():
        reserved_books = book_manager.getReserverdBooksByUser(user_manager.user.uid())
        user_books = [b for b in reserved_books['user_books'].split(',') if b]

    return render_template("books.html", books=books, user_books=user_books, g=g)

@book_view.route('/books/add/<int:id>', methods=['GET'])
def add(id):
    user_manager = get_user_manager()
    book_manager = get_book_manager()
    user_id = user_manager.user.uid()

    result = book_manager.reserve(user_id, id)
    if result == "err_out":
        msg = "Book not available"
    else:
        msg = "Book reserved"

    books = book_manager.list()
    reserved_books = book_manager.getReserverdBooksByUser(user_id)
    user_books = [b for b in reserved_books['user_books'].split(',') if b]

    return render_template("books.html", books=books, user_books=user_books, msg=msg, g=g)

@book_view.route('/books/search', methods=['GET'])
def search():
    user_manager = get_user_manager()
    book_manager = get_book_manager()
    user_manager.user.set_session(session, g)

    keyword = request.args.get("keyword", "")
    if not keyword:
        return redirect('/books')

    books = book_manager.search(keyword)
    user_books = []
    if user_manager.user.isLoggedIn():
        reserved_books = book_manager.getReserverdBooksByUser(user_manager.user.uid())
        user_books = [b for b in reserved_books['user_books'].split(',') if b]

    if books:
        return render_template("books.html", books=books, search=True, count=len(books), keyword=keyword, user_books=user_books, g=g)

    return render_template("books.html", error="No books found!", keyword=keyword, user_books=user_books, g=g)
