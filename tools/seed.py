import argparse
from app import create_app
from app.extensions import db
from app.models import User, Role, Category, Author, Book, BookAuthor


def ensure_roles():
	for r in ["admin", "staff", "student"]:
		if not Role.query.filter_by(name=r).first():
			db.session.add(Role(name=r))


def ensure_admin(password: str):
	u = User.query.filter_by(email="admin@example.com").first()
	if not u:
		u = User(email="admin@example.com", full_name="Admin", type="admin")
		db.session.add(u)
	u.set_password(password)
	return u


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--password", default="Admin@123", help="Admin password to set")
	parser.add_argument("--with-books", action="store_true", help="Seed sample categories, authors, and books")
	args = parser.parse_args()

	app = create_app()
	with app.app_context():
		db.create_all()
		ensure_roles()
		u = ensure_admin(args.password)
		if args.with_books:
			# Seed categories
			cat_names = ["Fiction", "Science", "Programming"]
			cats = {}
			for name in cat_names:
				c = Category.query.filter_by(name=name).first()
				if not c:
					c = Category(name=name)
					db.session.add(c)
					db.session.flush()
				cats[name] = c
			# Seed authors
			author_names = ["Jane Doe", "John Smith", "Linus Torvalds"]
			authors = {}
			for name in author_names:
				a = Author.query.filter_by(full_name=name).first()
				if not a:
					a = Author(full_name=name)
					db.session.add(a)
					db.session.flush()
				authors[name] = a
			# Seed books
			samples = [
				("9780000000011", "Sample Novel", "Fiction", ["Jane Doe"], 5),
				("9780000000028", "Physics Basics", "Science", ["John Smith"], 3),
				("9780000000035", "Intro to Git", "Programming", ["Linus Torvalds"], 4),
			]
			for isbn, title, cat_name, auth_names, copies in samples:
				if not Book.query.filter_by(isbn=isbn).first():
					b = Book(isbn=isbn, title=title, category=cats[cat_name], total_copies=copies, available_copies=copies)
					db.session.add(b)
					db.session.flush()
					for an in auth_names:
						db.session.add(BookAuthor(book_id=b.id, author_id=authors[an].id))
		db.session.commit()
		print(f"Admin ensured: {u.email} / {args.password}")
		if args.with_books:
			print("Seeded sample books.")


if __name__ == "__main__":
	main()

