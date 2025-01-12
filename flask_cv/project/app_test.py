from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure the SQLite database URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Post {self.title}>"

# Function to create the database and tables
def create_tables():
    with app.app_context():  # Ensure we have an app context
        print("Checking for database and tables...")
        if not os.path.exists('posts.db'):
            print("Database does not exist. Creating...")
        db.create_all()
        print("Tables created successfully.")

# Call the table creation function
create_tables()

@app.route('/')
def index():
    return "Welcome to the Post App!"

if __name__ == '__main__':
    app.run(debug=True)
