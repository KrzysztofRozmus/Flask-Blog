from flaskblog import app, db, bcrypt, login_manager
from flaskblog.forms import SignupForm, LoginForm
from flaskblog.models import User
from datetime import timedelta
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, login_fresh, current_user


@login_manager.user_loader
def load_user(email):
    return User.query.get(email)



@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")



@app.route("/signup", methods=["GET", "POST"])
def signup():    
    form = SignupForm()
    
    if current_user.is_authenticated:
        return redirect(url_for("user_dashboard"))
    
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
    
    if current_user.is_authenticated and login_fresh == True:
        return redirect(url_for("user_dashboard"))

    elif current_user.is_authenticated and login_fresh == False:
        return redirect(url_for("login"))
        
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        user_password = bcrypt.check_password_hash(user.password, form.password.data)
        
        if user_password:
            login_user(user, remember=True, duration=timedelta(minutes=1))
            flash(f"Logged in successfully. Hello {user.username}", "success")        
            return redirect(url_for("user_dashboard"))
        else:
            flash("Wrong password", "danger")
            return redirect(url_for("login"))
    else:       
        return render_template("login.html", form=form)    
    
    

@app.route("/user_dashboard", methods=["GET", "POST"])
@login_required
def user_dashboard():
    return render_template("user_dashboard.html")



@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been log out", "success")
    return redirect(url_for("login"))