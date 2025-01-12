# Run: python app_cv.py  in terminal from project root folder, or Run from Python IDE
"""
This is a Curriculum Vitae (CV) generator app that allows users to input titles and descriptions for education, work, hobbies, and other relevant entries. The idea is for users to compile a comprehensive list of their life events, career achievements, successes, certifications, and more. They can then select and customize an optimized list to create tailored CVs for specific job applications.

Restarting the app will remember the previously stored entries!

Flask app fundamentals copied from: https://github.com/mjhea0/flaskr-tdd/
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
redirecting, url_db handling, aborting requests, and returning JSON responses.

Imports SQLAlchemy for database interactions with SQLite database.
The rest of the file contains the application configuration, 
route definitions, and database models.

GET and POST Requests Handling: using SQLAlchemy ORM

LOGIN and LOGOUT
Use admin / admin as the username/password to login. Others will be rejected.
Modify the username and password in the app.config dictionary for security reasons.

Flash Messages: in case of errors or successful operations.
Appears on the web page, only once.

Module's in-built dependencies in the package folder: 
[pythonpackagefolder]\Lib\site-packages\
for example:
...\anaconda3_10\Lib\site-packages\flask\app.py
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

# create and initialize a new Flask app
app = Flask(__name__)
# load the config
app.config.from_object(__name__)

# config start ____________________________________________________

basedir = str(Path(__file__).resolve().parent).replace("\\", "/")
DATABASE = "cv.db"
url_db = os.getenv("DATABASE_url_db", f"sqlite:///{os.path.join(basedir, DATABASE)}") #{Path(basedir).joinpath(DATABASE)}")

SQLALCHEMY_DATABASE_URI = url_db
SQLALCHEMY_TRACK_MODIFICATIONS = False
"""SQLALCHEMY_TRACK_MODIFICATIONS:
Purpose: This configuration option is used to enable or disable the signaling support of SQLAlchemy.
Default Value: By default, it is set to None, which means it will follow the value of 
SQLALCHEMY_TRACK_MODIFICATIONS in the Flask-SQLAlchemy extension.
When set to True: SQLAlchemy will track modifications of objects and emit signals. This can be useful for0
 debugging or for certain extensions that need to know when changes occur.
When set to False: Disables the modification tracking system, which can save a significant amount of memory 
and improve performance.
"""

app.config['SQLALCHEMY_DATABASE_URI'] = url_db #'sqlite:///.../cv.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# init sqlalchemy with Flask application instance
# Binding the SQLAlchemy instance to the Flask app, 
# allowing the app to use SQLAlchemy for database interactions.

app.config['USERNAME'] = "admin" # for security reasons store and encrypt elsewhere
app.config['PASSWORD'] = "admin" # for security reasons store and encrypt elsewhere
app.config['SECRET_KEY'] = "change_me"

# config end ________________________________________________________

db = SQLAlchemy(app)

#from project import models
#from models import models

class Post(db.Model):
    """A post with an id, title, text, and type. 
    Order of the information parts in SQL query in INSERTION (add) case
    should be the same as the order of the table fields below."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String, nullable=False)
    type = db.Column(db.String(50), nullable=False)

    #db.create_all()
    # __init__ method to initialize the Post object with title, text, and type attributes.
    def __init__(self, title, text, type):
        self.title = title
        self.text = text,
        self.type = type

if url_db is None or not os.path.exists(url_db.replace("sqlite:///", "")):
    #import app_dbcreate # silented
    
    print("Database does not exist. Creating...") #prompt output, can be neglected
    with app.app_context():  # Push the application context
        db.create_all()
        

#if url_db.startswith("postgres://"):
#    url_db = url_db.replace("postgres://", "postgresql://", 1)


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
    """Searches the database for entries, then displays them.
    entries = None
    entries = db.session.query(Post) #models.Post
    if entries is None:
        print("No entries found.")
        return render_template("index.html", entries=None)
    else:
        entries = check_entries(entries)
        return render_template("index.html", entries=entries)
    """
    if request.method == "POST":
        # Retrieve form inputs
        title = request.form.get("title")
        text = request.form.get("text")
        post = request.form.get("type")

        # Sanitize inputs
        title = title[0] if isinstance(title, tuple) else title
        text = text[0] if isinstance(text, tuple) else text
        type = type[0] if isinstance(type, tuple) else type

        # Handle empty or None values
        title = title.strip() if title else ""
        text = text.strip() if text else ""
        type = type.strip() if type else ""

        # Create a new Post object
        new_entry = Post(title=title, text=text, type=type)
        db.session.add(new_entry)
        db.session.commit()

        return redirect(url_for("index") )

    # Fetch all posts
    entries = Post.query.all()
    return render_template("index.html", entries=entries)


@app.route("/add", methods=["POST"])
def add_entry():
    """Adds new post to the database."""
    if not session.get("logged_in"):
        abort(401)

    # should follow the same order as the class Post(db.Model):
    # title, text, type
    new_entry = Post(request.form["title"], request.form["text"], request.form["type"])
    # text written in the 'text' form field may turn to a tuple, convert it to a string
    new_entry.text = ''.join(new_entry.text) if isinstance(new_entry.text, tuple) else new_entry.text
    db.session.add(new_entry)
    db.session.commit()
    flash("New entry was successfully posted")
    return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    """User login/authentication/session management."""
    error = None   
    username = request.form.get('username')
    if username is None or username == 'username' or username == '': #empty form cases
        flash("Wrong username or password")
        return render_template("login.html")
    if request.form.get('username') != app.config["USERNAME"]:
        error = "Invalid username"
    elif request.form.get('password') != app.config["PASSWORD"]:
        error = "Invalid password"
    else:
        session["logged_in"] = True
        flash("You were logged in")
        return redirect(url_for("index"))
    if request.method == "GET":
        return render_template("login.html", error=error)
    else: # request.method == "POST", double safety branch, not needed
        return render_template("index.html")
    
@app.route("/logout")
def logout():
    """User logout/authentication/session management."""
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("index"))

@app.route("/delete/<int:post_id>", methods=["GET"])
@login_required
# The login_required decorator ensures that the user is logged in before proceeding.
def delete_entry(post_id):
    """Deletes post from database based on database id."""
    result = {"status": 0, "message": "Error"}
    try:
        new_id = post_id
        db.session.query(Post).filter_by(id=new_id).delete() # models.Post
        db.session.commit()
        result = {"status": 1, "message": "Post Deleted"}
        #Flash (one-time) message sent to the user
        flash("The entry was deleted.")
    except Exception as e:
        result = {"status": 0, "message": repr(e)}
        flash(f"An error occurred: {repr(e)}", "error")
    #return jsonify(result) # for debugging
    return redirect(url_for("index")) # return to the main page with updated entries

@app.route("/search/", methods=["GET"])
def search():
    """Displays search form and results."""
    query = request.args.get("query")
    entries = db.session.query(Post) #models.Post
    if query:
        return render_template("search.html", entries=entries, query=query)
    return render_template("search.html")

@app.route("/help")
def help():
    """Displays helpful static page."""
    return render_template("help.html")

if __name__ == "__main__":
    app.run(debug=True)