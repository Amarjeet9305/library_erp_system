from flask import Blueprint, g, session, redirect, render_template, request, jsonify, Response, current_app
from markupsafe import escape
from Misc.functions import *
from Controllers.AdminManager import AdminManager
from Controllers.BookManager import BookManager
from Controllers.UserManager import UserManager

# Blueprint setup
admin_view = Blueprint('admin_routes', __name__, template_folder='../templates/admin/', url_prefix='/admin')

# Helper functions to get managers to avoid circular imports
def get_admin_manager():
    DAO = current_app.config.get('DAO')
    return AdminManager(DAO)

def get_book_manager():
    DAO = current_app.config.get('DAO')
    return BookManager(DAO)

def get_user_manager():
    DAO = current_app.config.get('DAO')
    return UserManager(DAO)

# Routes
@admin_view.route('/', methods=['GET'])
def home():
    admin_manager = get_admin_manager()
    admin_manager.admin.set_session(session, g)
    return render_template('admin/home.html', g=g)

@admin_view.route('/signin/', methods=['GET', 'POST'])
def signin():
    admin_manager = get_admin_manager()
    g.bg = 1

    if request.method == 'POST':
        _form = request.form
        email = str(_form["email"])
        password = str(_form["password"])

        if len(email) < 1 or len(password) < 1:
            return render_template('admin/signin.html', error="Email and password are required")

        d = admin_manager.signin(email, hash(password))

        if d and len(d) > 0:
            session['admin'] = int(d["id"])
            return redirect("/admin")

        return render_template('admin/signin.html', error="Email or password incorrect")

    return render_template('admin/signin.html')

@admin_view.route('/signout/', methods=['GET'])
def signout():
    admin_manager = get_admin_manager()
    admin_manager.signout()
    return redirect("/admin/", code=302)

@admin_view.route('/users/view/', methods=['GET'])
def users_view():
    admin_manager = get_admin_manager()
    admin_manager.admin.set_session(session, g)

    id = int(admin_manager.admin.uid())
    admin = admin_manager.get(id)
    myusers = admin_manager.getUsersList()

    return render_template('users.html', g=g, admin=admin, users=myusers)

@admin_view.route('/books/', methods=['GET'])
def books():
    admin_manager = get_admin_manager()
    book_manager = get_book_manager()
    admin_manager.admin.set_session(session, g)

    id = int(admin_manager.admin.uid())
    admin = admin_manager.get(id)
    mybooks = book_manager.list(availability=0)

    return render_template('books/views.html', g=g, books=mybooks, admin=admin)

@admin_view.route('/books/<int:id>')
def view_book(id):
    admin_manager = get_admin_manager()
    book_manager = get_book_manager()
    user_manager = get_user_manager()

    admin_manager.admin.set_session(session, g)

    if id is not None:
        b = book_manager.getBook(id)
        users = user_manager.getUsersByBook(id)

        if b and len(b) < 1:
            return render_template('books/book_view.html', error="No book found!")

        return render_template("books/book_view.html", books=b, books_owners=users, g=g)

@admin_view.route('/books/add', methods=['GET', 'POST'])
def book_add():
    admin_manager = get_admin_manager()
    admin_manager.admin.set_session(session, g)
    return render_template('books/add.html', g=g)

@admin_view.route('/books/edit/<int:id>', methods=['GET', 'POST'])
def book_edit(id):
    admin_manager = get_admin_manager()
    book_manager = get_book_manager()
    admin_manager.admin.set_session(session, g)

    if id is not None:
        b = book_manager.getBook(id)

        if b and len(b) < 1:
            return render_template('edit.html', error="No book found!")

        return render_template("books/edit.html", book=b, g=g)

    return redirect('/books')

@admin_view.route('/books/delete/<int:id>', methods=['GET'])
def book_delete(id):
    book_manager = get_book_manager()

    if id is not None:
        book_manager.delete(id)

    return redirect('/admin/books/')

@admin_view.route('/books/search', methods=['GET'])
def search():
    admin_manager = get_admin_manager()
    book_manager = get_book_manager()
    admin_manager.admin.set_session(session, g)

    if "keyword" not in request.args:
        return render_template("books/view.html")

    keyword = request.args["keyword"]

    if len(keyword) < 1:
        return redirect('/admin/books')

    id = int(admin_manager.admin.uid())
    admin = admin_manager.get(id)

    d = book_manager.search(keyword, 0)

    if len(d) > 0:
        return render_template("books/views.html", search=True, books=d, count=len(d), keyword=escape(keyword), g=g, admin=admin)

    return render_template('books/views.html', error="No books found!", keyword=escape(keyword))
