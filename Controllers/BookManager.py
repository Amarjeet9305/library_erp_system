from App.Books import Books

class BookManager():
    def __init__(self, DAO):
        self.book_dao = Books(DAO.db.book).dao

    def add(self, book_info):
        return self.book_dao.add(book_info)

    def delete(self, book_id):
        return self.book_dao.delete(book_id)

    def update(self, book_id, book_info):
        return self.book_dao.update(book_id, book_info)

    def list(self, availability=None, user_id=None):
        if user_id:
            return self.book_dao.getBooksByUser(user_id)
        return self.book_dao.list(availability)

    def getBook(self, book_id):
        return self.book_dao.getBook(book_id)

    def search(self, keyword, availability=None):
        return self.book_dao.search_book(keyword, availability)

    def reserve(self, user_id, book_id):
        return self.book_dao.reserve(user_id, book_id)

    def getReserverdBooksByUser(self, user_id):
        return self.book_dao.getReserverdBooksByUser(user_id)
