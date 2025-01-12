# run the app with: python app.py  in terminal, or use the run button in a Python editor (IDE)
"""
This application runs on local server (http://127.0.0.1:5000) and uses SQLite Database server to store posted entries for a Cookbook.

Restarting the app will remember the previously stored entries!

Main application and routing logic for Flask app
fundamentals from: https://github.com/mjhea0/flaskr-tdd/
and
https://github.com/realpython/discover-flask?tab=readme-ov-file

Imports and Setup:
Imports necessary modules and functions from Python's standard library and 
Flask framework.
Sets up the main application and routing logic for a Flask app.
Flask and SQLAlchemy:

Uses Flask (python module) to create the web application (local: http://127.0.0.1:5000/).
Imports from Flask module:
- render_template,
- request,
- session,
- flash,
- redirect,
- url_for,
- abort,
- jsonify
for handling various web functionalities like rendering 
HTML templates, handling requests and sessions, flashing messages, 
redirecting, URL handling, aborting requests, and returning JSON responses.

Imports SQLAlchemy for database interactions with SQLite database.
The rest of the file contains the application configuration, 
route definitions, and database models.

GET and POST Requests: handled by the SQLAlchemy.

Flash Messages: used to display messages to the user. Appears only once on the loaded page.

LOGIN and LOGOUT
use admin/admin as the username/password to login.
"""

import os
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    render_template,
    request,
    session,
    flash,
    redirect,
    url_for,
    abort,
    jsonify,
)

from flask_sqlalchemy import SQLAlchemy

# configuration ____________________________________________________
basedir = Path(__file__).resolve().parent

DATABASE = "flaskr.db"
USERNAME = "admin" # for security reasons store and encrypt elsewhere
PASSWORD = "admin" # for security reasons store and encrypt elsewhere
SECRET_KEY = "change_me"

url = os.getenv("DATABASE_URL", f"sqlite:///{Path(basedir).joinpath(DATABASE)}")

if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_DATABASE_URI = url
SQLALCHEMY_TRACK_MODIFICATIONS = False
# config end ________________________________________________________

# create and initialize a new Flask app
app = Flask(__name__)
# load the config
app.config.from_object(__name__)
# init sqlalchemy with Flask application instance
# Binding the SQLAlchemy instance to the Flask app, 
# allowing the app to use SQLAlchemy for database interactions.
db = SQLAlchemy(app)

#from project import models
from models import models

def login_required(f):
    """Decorator to ensure user is logged in before proceeding."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Please log in.")
            return jsonify({"status": 0, "message": "Please log in."}), 401
        return f(*args, **kwargs)

    return decorated_function

@app.route("/")
def index():
    """Searches the database for entries, then displays them."""
    entries = db.session.query(models.Post)
    return render_template("index.html", entries=entries)

@app.route("/add", methods=["POST"])
def add_entry():
    """Adds new post to the database."""
    if not session.get("logged_in"):
        abort(401)
    new_entry = models.Post(request.form["title"], request.form["text"])
    db.session.add(new_entry)
    db.session.commit()
    flash("New entry was successfully posted")
    return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    """User login/authentication/session management."""
    error = None
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            error = "Invalid username"
        elif request.form["password"] != app.config["PASSWORD"]:
            error = "Invalid password"
        else:
            session["logged_in"] = True
            flash("You were logged in")
            return redirect(url_for("index"))
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    """User logout/authentication/session management."""
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("index"))

@app.route("/delete/<int:post_id>", methods=["GET"])
@login_required
def delete_entry(post_id):
    """Deletes post from database."""
    result = {"status": 0, "message": "Error"}
    try:
        new_id = post_id
        db.session.query(models.Post).filter_by(id=new_id).delete()
        db.session.commit()
        result = {"status": 1, "message": "Post Deleted"}
        flash(["The entry post_id: ", str(post_id), "was deleted."])
    except Exception as e:
        result = {"status": 0, "message": repr(e)}
        flash("error", result)
    return jsonify(result)

@app.route("/search/", methods=["GET"])
def search():
    """Displays search form and results.
    partial match search, in title or text is defined in search.html"""
    query = request.args.get("query")
    entries = db.session.query(models.Post)
    if query:
        return render_template("search.html", entries=entries, query=query)
    return render_template("search.html")

@app.route("/help")
def help():
    """Displays a helpful static page."""
    return render_template("help.html")

if __name__ == "__main__":
    app.run()