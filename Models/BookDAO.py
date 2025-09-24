class BookDAO():
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = "books"

    # Add new book
    def add(self, book_info):
        query = """
        INSERT INTO @table (name, `desc`, author, availability, edition, count)
        VALUES ('{}','{}','{}', {}, '{}', {})
        """.format(
            book_info['name'], book_info['desc'], book_info['author'],
            book_info.get('availability', 1),
            book_info.get('edition', '1'),
            book_info.get('count', 1)
        )
        self.db.query(query)
        self.db.commit()
        return True

    # Delete a book by ID
    def delete(self, id):
        self.db.query("DELETE FROM @table WHERE id={}".format(id))
        self.db.commit()

    # Update a book
    def update(self, id, book_info):
        query = """
        UPDATE @table SET name='{}', `desc`='{}', author='{}', availability={}, edition='{}', count={}
        WHERE id={}
        """.format(
            book_info['name'], book_info['desc'], book_info['author'],
            book_info.get('availability', 1),
            book_info.get('edition', '1'),
            book_info.get('count', 1),
            id
        )
        self.db.query(query)
        self.db.commit()

    # Get a book by ID
    def getBook(self, id):
        return self.db.query("SELECT * FROM @table WHERE id={}".format(id)).fetchone()

    # List all books
    def list(self, availability=None):
        query = "SELECT * FROM @table"
        if availability is not None:
            query += " WHERE availability={}".format(availability)
        return self.db.query(query).fetchall()

    # Search books by name
    def search_book(self, name, availability=None):
        query = "SELECT * FROM @table WHERE name LIKE '%{}%'".format(name)
        if availability is not None:
            query += " AND availability={}".format(availability)
        return self.db.query(query).fetchall()

    # Reserve a book for a user
    def reserve(self, user_id, book_id):
        book = self.getBook(book_id)
        if not book or book['count'] < 1:
            return "err_out"

        self.db.query("INSERT INTO reserve (user_id, book_id) VALUES({}, {})".format(user_id, book_id))
        self.db.query("UPDATE @table SET count=count-1 WHERE id={}".format(book_id))
        self.db.commit()
        return True

    # Get books reserved by user
    def getReserverdBooksByUser(self, user_id):
        query = "SELECT GROUP_CONCAT(book_id) AS user_books FROM reserve WHERE user_id={}".format(user_id)
        result = self.db.query(query).fetchone()
        return {'user_books': result['user_books'] or ''}

    # Get books by user
    def getBooksByUser(self, user_id):
        query = """
        SELECT @table.* FROM @table
        JOIN reserve ON reserve.book_id=@table.id
        WHERE reserve.user_id={}
        """.format(user_id)
        return self.db.query(query).fetchall()
