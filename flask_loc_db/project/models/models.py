from app import db

class Post(db.Model):
    """Post model for database table with columns id, title, text
    SQL query information order should be the same as the order of attributes"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)

    def __init__(self, title, text):
        """Initializes the Post object with title"""
        self.title = title
        self.text = text

    def __repr__(self):
        return f"<title {self.title}>"
