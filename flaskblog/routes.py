from flaskblog import app
from flaskblog.forms import SignupForm, LoginForm
from flask import render_template, redirect, url_for, flash

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    
    if form.validate_on_submit():
        flash("The account was successfully created", "success")
        return redirect(url_for("login"))
    else:
        return render_template('signup.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        flash("Logged in successfully", "success")        
        return redirect(url_for("home"))
    else:       
        return render_template("login.html", form=form)