from App.Admin import Admin

class AdminManager():
    def __init__(self, DAO):
        # Admin object manages admin session and DAO
        self.admin = Admin(DAO.db.admin)  
        # User DAO to fetch user data
        self.user = DAO.db.user            
        # Admin DAO for database queries
        self.dao = self.admin.dao          

    # Admin sign-in method
    def signin(self, email, password):
        admin = self.dao.getByEmail(email)

        if not admin:
            return False

        if admin["password"] != password:
            return False

        return admin

    # Get admin details by id
    def get(self, id):
        return self.dao.getById(id)

    # Get list of all users
    def getUsersList(self):
        users = self.user.list()
        return users

    # Sign out admin
    def signout(self):
        self.admin.signout()

    # Fetch list of users (alias)
    def user_list(self):
        return self.user.list()

    # Fetch a single user by ID
    def getUser(self, id):
        return self.user.getById(id)

    # Add a new user (optional if needed)
    def addUser(self, name, email, password, bio="", mob=""):
        return self.user.addUser(name, email, password, bio, mob)

    # Fetch books for admin view (optional utility)
    def getBooksList(self, availability=1):
        return self.admin.book.list(availability)

    # Search books (optional utility)
    def searchBooks(self, keyword, availability=1):
        return self.admin.book.search_book(keyword, availability)
