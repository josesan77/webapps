"""
A helper script to create the database and tables for a Flask application.
Use only if app_cv.py is not working, or it fails to create the database and tables.

This script sets up a Flask application with an SQLite database using SQLAlchemy.
It defines a `Post` model with `id`, `title`, `text`, and `type` fields, and ensures
the database and table are created when the script is run.
Modules:
    flask: Provides the Flask class to create the application.
    flask_sqlalchemy: Provides the SQLAlchemy class to handle database operations.
    pathlib: Provides the Path class to handle filesystem paths.
    os: Provides a way to interact with the operating system.
Functions:
    None
Classes:
    Post: A SQLAlchemy model representing a post with an id, title, and content.
Usage:
    Run this script directly to create the database and tables.
"""
# Placeholder for any necessary imports or initializations
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
import os

app = Flask(__name__) # Create/instantiate a Flask application

# Configure SQLite database (in the same directory as this script)
basedir = Path(__file__).resolve().parent
DATABASE = 'posts.db'
# url/database path is declared to be in the project root directory 
url = os.getenv("DATABASE_URL", f"sqlite:///{Path(basedir).joinpath(DATABASE)}")
app.config['SQLALCHEMY_DATABASE_URI'] = url #'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)
#print(url) # use only for debugging in terminal

# Define the Post model
class Post(db.Model):
    """ A post with an id, title, text, and type. 
    Order of the information parts in SQL query in INSERTION (add) case
    should be the same as the order of the table fields below."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String, nullable=False)
    type = db.Column(db.String(50), nullable=False)

# Ensure the database and table are created
if __name__ == '__main__':
    with app.app_context():  # Push the application context
        db.create_all()  # Create the database and tables
        print("Database and tables created successfully.")
