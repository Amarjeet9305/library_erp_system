from flask import Flask
from markupsafe import escape
from Misc.functions import *

app = Flask(__name__)
app.secret_key = '#$ab9&^BB00_.'  # your secret key

# -----------------------------
# Initialize DAO and store in app config
# -----------------------------
from Models.DAO import DAO
DAO_instance = DAO(app)
app.config['DAO'] = DAO_instance

# -----------------------------
# Registering blueprints
# -----------------------------
# Import after DAO creation to avoid circular imports
from routes.user import user_view
from routes.book import book_view
from routes.admin import admin_view

app.register_blueprint(user_view)
app.register_blueprint(book_view)
app.register_blueprint(admin_view)

# -----------------------------
# Registering custom functions for templates
# -----------------------------
app.jinja_env.globals.update(
    ago=ago,
    str=str,
    escape=escape  # make escape available in Jinja templates
)

# -----------------------------
# Run the app
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
