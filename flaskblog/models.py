from flaskblog import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.png")
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.now())
    posts = db.relationship("Post", backref="user")
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        
    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
            
    
    
class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id
    
    def __repr__(self) -> str:
        return f"User('{self.title}', '{self.content}', '{self.user_id}')"