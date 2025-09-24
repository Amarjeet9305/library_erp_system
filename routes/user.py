from flask import Blueprint, g, session, redirect, render_template, request, jsonify, Response, flash, current_app
from markupsafe import escape
from Misc.functions import *
from Controllers.UserManager import UserManager

# Blueprint setup
user_view = Blueprint('user_routes', __name__, template_folder='/templates')

# Initialize UserManager inside a function to avoid circular imports
def get_user_manager():
    DAO = current_app.config.get('DAO')  # ✅ access DAO from app config
    return UserManager(DAO)

# Routes
@user_view.route('/', methods=['GET'])
def home():
    g.bg = 1
    user_manager = get_user_manager()
    user_manager.user.set_session(session, g)
    print(g.user)
    return render_template('home.html', g=g)

@user_view.route('/signin', methods=['GET', 'POST'])
def signin():
    user_manager = get_user_manager()
    if request.method == 'POST':
        _form = request.form
        email = str(_form["email"])
        password = str(_form["password"])

        if len(email) < 1 or len(password) < 1:
            return render_template('signin.html', error="Email and password are required")

        d = user_manager.signin(email, hash(password))

        if d and len(d) > 0:
            session['user'] = int(d['id'])
            return redirect("/")

        return render_template('signin.html', error="Email or password incorrect")

    return render_template('signin.html')

@user_view.route('/signup', methods=['GET', 'POST'])
def signup():
    user_manager = get_user_manager()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if len(name) < 1 or len(email) < 1 or len(password) < 1:
            return render_template('signup.html', error="All fields are required")

        new_user = user_manager.signup(name, email, hash(password))

        if new_user == "already_exists":
            return render_template('signup.html', error="User already exists with this email")

        return render_template('signup.html', msg="You've been registered!")

    return render_template('signup.html')

@user_view.route('/signout/', methods=['GET'])
def signout():
    user_manager = get_user_manager()
    user_manager.signout()
    return redirect("/", code=302)

@user_view.route('/user/', methods=['GET'])
def show_user(id=None):
    user_manager = get_user_manager()
    user_manager.user.set_session(session, g)

    if id is None:
        id = int(user_manager.user.uid())

    d = user_manager.get(id)
    mybooks = user_manager.getBooksList(id)

    return render_template("profile.html", user=d, books=mybooks, g=g)

@user_view.route('/user', methods=['POST'])
def update():
    user_manager = get_user_manager()
    user_manager.user.set_session(session, g)

    _form = request.form
    name = str(_form["name"])
    email = str(_form["email"])
    password = str(_form["password"])
    bio = str(_form["bio"])

    user_manager.update(name, email, hash(password), bio, user_manager.user.uid())

    flash('Your info has been updated!')
    return redirect("/user/")
