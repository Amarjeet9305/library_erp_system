import os
from flask import Flask, render_template
from dotenv import load_dotenv
from .config import Config
from .extensions import db, migrate, login_manager, csrf


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    # Ensure instance directory exists and normalize SQLite path to absolute
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except Exception:
        pass

    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    # If pointing to a relative SQLite DB (e.g., sqlite:///instance/library.db),
    # resolve it to an absolute path under app.instance_path to avoid OS path issues
    if db_uri.startswith("sqlite:///instance/"):
        relative_part = db_uri[len("sqlite:///instance/"):]
        absolute_db_path = os.path.join(app.instance_path, relative_part)
        # Normalize backslashes for SQLAlchemy URI compatibility
        absolute_db_path = absolute_db_path.replace("\\", "/")
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{absolute_db_path}"

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from .blueprints.auth.routes import auth_bp
    from .blueprints.books.routes import books_bp
    from .blueprints.circulation.routes import circ_bp
    from .blueprints.reports.routes import reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp, url_prefix="/books")
    app.register_blueprint(circ_bp, url_prefix="/circulation")
    app.register_blueprint(reports_bp, url_prefix="/reports")

    @app.route("/")
    def index():
        from .models import Book, BookCopy, Transaction
        from sqlalchemy import func
        from datetime import date

        total_books = db.session.query(func.count(Book.id)).scalar() or 0
        total_copies = db.session.query(func.sum(Book.total_copies)).scalar() or 0
        available_copies = db.session.query(func.sum(Book.available_copies)).scalar() or 0
        issued_copies = db.session.query(func.count()).select_from(BookCopy).filter_by(status="issued").scalar() or 0
        overdue_copies = (
            db.session.query(func.count(Transaction.id))
            .filter(Transaction.status == "overdue")
            .scalar()
            or 0
        )
        stats = {
            "total_books": total_books,
            "total_copies": total_copies,
            "available_copies": available_copies,
            "issued_copies": issued_copies,
            "overdue_copies": overdue_copies,
        }
        return render_template("dashboard.html", stats=stats)

    # Ensure tables exist in dev/local
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            # On DB connectivity issues, we skip; errors will surface on use
            pass

    # CLI command to seed roles and an admin user
    @app.cli.command("seed-admin")
    def seed_admin():
        from .models import Role, User
        db.create_all()
        for r in ["admin", "staff", "student"]:
            if not Role.query.filter_by(name=r).first():
                db.session.add(Role(name=r))
        if not User.query.filter_by(email="admin@example.com").first():
            u = User(email="admin@example.com", full_name="Admin", type="admin")
            u.set_password("Admin@123")
            db.session.add(u)
        db.session.commit()
        print("Seeded roles and admin (admin@example.com / Admin@123)")

    # CLI command to reset admin password
    @app.cli.command("reset-admin")
    def reset_admin():
        from .models import User
        db.create_all()
        u = User.query.filter_by(email="admin@example.com").first()
        if not u:
            u = User(email="admin@example.com", full_name="Admin", type="admin")
            db.session.add(u)
        u.set_password("Admin@123")
        db.session.commit()
        print("Admin password reset to Admin@123 for admin@example.com")

    return app
