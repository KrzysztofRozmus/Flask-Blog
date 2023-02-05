from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from secrets import token_urlsafe


app = Flask(__name__)
app.secret_key = token_urlsafe(32)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
db.init_app(app)

bcrypt = Bcrypt(app)



from flaskblog import routes