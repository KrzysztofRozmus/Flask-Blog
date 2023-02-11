from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flaskblog.models import User
    

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),
                                                   Length(min=3, max=30)])
    
    # username = StringField(validators=[DataRequired(),
    #                                    Length(min=3, max=30)],
    #                                    render_kw={"placeholder": "Username"})
    
    email = EmailField("Email", validators=[DataRequired(),
                                            Email(),
                                            Length(min=5, max=30)])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=3, max=35)])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(),
                                                                     EqualTo("password", "Field must be equal to Password.")])
    submit = SubmitField("Create account")
    
    
    def validate_username(self, username):
        username = User.query.filter_by(username=username.data).first()
        if username:
            raise ValidationError("That username is already taken.", "danger")
        
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("That email is already taken.", "danger")
# ---------------------------------------------------------------------------------------------------------------------

    
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(),
                                            Email(),
                                            Length(min=5, max=30)])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=3, max=35)])
    submit = SubmitField("Login")
    
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if not email:
            raise ValidationError("Wrong email.", "danger")
# ---------------------------------------------------------------------------------------------------------------------


class ChangePasswordForm(FlaskForm):
        current_password = PasswordField("Current password", validators=[DataRequired(),
                                                     Length(min=3, max=35)])
        
        new_password = PasswordField("New password", validators=[DataRequired(),
                                                     Length(min=3, max=35)])
        
        confirm_new_password = PasswordField("Confirm new password", validators=[DataRequired(),
                                                                                 EqualTo("new_password", "Field must be equal to New password.")])
        submit = SubmitField("Change")
# ---------------------------------------------------------------------------------------------------------------------


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=80)])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Add Post")
# ---------------------------------------------------------------------------------------------------------------------

    
class ProfilePic(FlaskForm):
    pic_file = FileField("Update profile picture", validators=[FileRequired(), FileAllowed(["jpg", "png"])])
    update = SubmitField("Update")