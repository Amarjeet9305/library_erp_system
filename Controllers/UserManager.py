from App.User import User

class UserManager():
    def __init__(self, DAO):
        self.user = User(DAO.db.user)
        self.dao = self.user.dao
        self.book_dao = DAO.db.book  # for user-book relationships

    # List all users
    def list(self):
        return self.dao.list()

    # User login
    def signin(self, email, password):
        user = self.dao.getByEmail(email)
        if not user:
            return False

        if user['password'] != password:
            return False

        return user

    # User logout
    def signout(self):
        self.user.signout()

    # Get a single user by ID
    def get(self, id):
        return self.dao.getById(id)

    # Signup new user
    def signup(self, name, email, password, bio='', mob=''):
        existing_user = self.dao.getByEmail(email)
        if existing_user:
            return "already_exists"

        user_info = {
            "name": name,
            "email": email,
            "password": password,
            "bio": bio,
            "mob": mob,
            "lock": 0
        }
        return self.dao.add(user_info)

    # Update user info
    def update(self, name, email, password, bio, id):
        user_info = {
            "name": name,
            "email": email,
            "password": password,
            "bio": bio
        }
        return self.dao.update(user_info, id)

    # Get list of books reserved by user
    def getBooksList(self, user_id):
        return self.book_dao.getBooksByUser(user_id)

    # Get users who reserved a specific book
    def getUsersByBook(self, book_id):
        return self.dao.getUsersByBook(book_id)
