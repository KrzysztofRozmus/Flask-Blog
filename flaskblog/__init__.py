from flask import Flask
from secrets import token_urlsafe


app = Flask(__name__)
app.secret_key = token_urlsafe(32)



from flaskblog import routes