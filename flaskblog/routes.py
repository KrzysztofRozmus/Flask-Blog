from flaskblog import app, db, bcrypt, login_manager
from flaskblog.forms import SignupForm, LoginForm, PostForm, ProfilePic, ChangePasswordForm
from flaskblog.models import User, Post
from datetime import timedelta
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, login_fresh, current_user


@login_manager.user_loader
def load_user(email):
    return User.query.get(email)


@app.route("/")
@app.route("/home")
def home():
    image_file = url_for("static", filename="pictures/default_pic.png")
    posts = Post.query.all()    
    return render_template("index.html", posts=posts, image_file=image_file)


@app.route("/signup", methods=["GET", "POST"])
def signup():    
    form = SignupForm()
    
    if current_user.is_authenticated:
        return redirect(url_for("user_dashboard"))
    
    elif form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data,
                                                        14).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)  
                      
        db.session.add(user)
        db.session.commit()                
        flash("The account was successfully created. You can log in now.", "success")
        return redirect(url_for("login"))
    else:
        return render_template('signup.html', form=form)
    


@app.route("/login", methods=["GET", "POST"])
def login():    
    form = LoginForm()
    
    if current_user.is_authenticated:
        return redirect(url_for("user_dashboard"))
        
    elif form.validate_on_submit():
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
    form = PostForm()
    pic_form = ProfilePic()
          
    if form.validate_on_submit():
        
        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user)
                              
        db.session.add(post)
        db.session.commit()
        flash("The post was published", "info")
        return redirect(url_for("home"))
    else:
        image_file = url_for("static", filename="pictures/default_pic.png")
        return render_template("user_dashboard.html",
                               form=form,
                               image_file=image_file,
                               pic_form=pic_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been log out", "success")
    return redirect(url_for("login"))



@app.route("/delete_account/<email>")
@login_required
def delete_account(email):  
    
    if email == current_user.email:
              
        delete_query = User.query.filter_by(email=email).first()
        db.session.delete(delete_query)
        db.session.commit()        
        logout_user()
        
        flash("Account has been deleted", "info")
        return redirect(url_for("login"))    
    else:
        flash("Unauthorized activity", "danger")
        return redirect(url_for("user_dashboard"))
    
    
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        check_password = bcrypt.check_password_hash(current_user.password, form.current_password.data)
        
        if check_password and current_user.is_authenticated:
            hashed_new_password = bcrypt.generate_password_hash(form.new_password.data, 14).decode("utf-8")        
            User.query.filter_by(email=current_user.email).update(dict(password=hashed_new_password))
            db.session.commit()
            flash("Password has been changed successfully", "success")
            return redirect(url_for("user_dashboard"))
        else:
            flash("Wrong current password", "danger")
            return redirect(url_for("change_password"))        
    else:
        return render_template("change_password.html", form=form)