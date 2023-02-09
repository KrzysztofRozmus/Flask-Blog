from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from secrets import token_urlsafe


app = Flask(__name__)
app.secret_key = token_urlsafe(32)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
db.init_app(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

my_datetime = datetime.now()
current_datetime = my_datetime.replace(microsecond = 0)


# If user is not logged in and want to access page with login_required decorator,
# the login_view redirects him to login page with login_message message.
login_manager.login_view = "login"
login_manager.login_message = "You have to log in first!"
login_manager.login_message_category = "info"


from flaskblog import routes