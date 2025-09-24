import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "dev-salt")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "mysql+mysqldb://lib_user:strong_password@127.0.0.1:3306/library_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False") == "True"

    REMEMBER_COOKIE_DURATION = timedelta(days=int(os.getenv("REMEMBER_COOKIE_DURATION_DAYS", "14")))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False") == "True"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
