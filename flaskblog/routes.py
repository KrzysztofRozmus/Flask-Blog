from flaskblog import app
from flask import render_template, redirect, request

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/login")
def login():
    return render_template("login.html")