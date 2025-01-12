from app_cv import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String, nullable=False)
    type = db.Column(db.String(50), nullable=False)

    #db.create_all()

    def __init__(self, title, text, type):
        self.title = title
        self.text = text,
        self.type = type

    """
    # Function to create tables if the database doesn't exist
    def create_tables():
        with app.app_context():  # Explicitly push an application context
            if not os.path.exists('posts.db'):
                print("Database does not exist. Creating...")
                db.create_all()
            else:
                print("Database already exists.")
    """

    def __repr__(self):
        return f"<title {self.title}>"
