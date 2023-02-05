from flaskblog import app, db, bcrypt
from flaskblog.forms import SignupForm, LoginForm
from flaskblog.models import User
from flask import render_template, redirect, url_for, flash

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")



@app.route("/signup", methods=["GET", "POST"])
def signup():    
    form = SignupForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data,
                                                        14).decode("utf-8")
        user = User(form.username.data,
                    form.email.data,
                    hashed_password,
                    )
        
        db.session.add(user)
        db.session.commit()        
        flash("The account was successfully created. You can log in now.", "success")
        return redirect(url_for("login"))
    else:
        return render_template('signup.html', form=form)    
    


@app.route("/login", methods=["GET", "POST"])
def login():    
    form = LoginForm()  
    
    if form.validate_on_submit():  
        user = User(form.email.data)   
        flash(f"Logged in successfully {user.username}", "success")        
        return redirect(url_for("home"))
    else:       
        return render_template("login.html", form=form)