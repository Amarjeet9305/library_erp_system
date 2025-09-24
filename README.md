## ERP Library Management System (Flask + MySQL)

### System requirements
- **Hardware**: 2 CPU, 4 GB RAM minimum; SSD storage; 10 GB free disk
- **Software**:
  - Python 3.11+
  - MySQL 8.0+
  - pip, virtualenv (optional)
  - Git (optional)
  - Windows, macOS, or Linux

### Quick start (local)
```bash
# 1) Create virtual environment
python -m venv .venv

# 2) Activate
# PowerShell
. .venv\Scripts\Activate.ps1

# 3) Install dependencies
pip install -r requirements.txt

# 4) Configure environment variables
# create .env in project root (see .env.example)

# 5) Create database and schema
# Update .env with DB credentials first, then run:
flask db upgrade
# Alternatively, run raw SQL from sql/01_schema.sql

# 6) Run
set FLASK_APP=run.py
set FLASK_ENV=development
flask run
```

### Security measures
- **Password hashing** using Werkzeug (PBKDF2) via Flask-Login compatible `User` model.
- **SQL injection prevention** via SQLAlchemy ORM and parameterized queries.
- **CSRF protection** via Flask-WTF on all forms.
- **Session protection** with `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SECURE` (enable on HTTPS), and `PERMANENT_SESSION_LIFETIME`.
- **Least privilege DB user** with limited grants.
- **Input validation** and server-side authorization checks (roles: admin/staff/student).
- **Audit fields** on core tables (`created_at`, `updated_at`).

### Project structure
```
app/
  __init__.py
  config.py
  extensions.py
  models/
    __init__.py
    user.py
    catalog.py
    circulation.py
  utils/
    __init__.py
    fines.py
  blueprints/
    auth/
      __init__.py
      routes.py
      forms.py
    books/
      __init__.py
      routes.py
      forms.py
    circulation/
      __init__.py
      routes.py
      forms.py
    reports/
      __init__.py
      routes.py
  templates/
    layout.html
    dashboard.html
    login.html
    books/
      list.html
      form.html
    circulation/
      issue.html
      return.html
  static/
    css/
      main.css
migrations/        # auto-created after first migrate init
sql/
  01_schema.sql
run.py
.env.example
```

### ER diagram
See `docs/erd.md` for a Mermaid diagram and explanation.

### Reports
- Daily/Weekly/Monthly circulation summaries and fines collected.
- Export to CSV available via simple endpoints.

### Notes
- Use `Flask-Migrate` for schema evolution.
- Seed initial roles and an admin user after first run.
