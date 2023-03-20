from flask_wtf import  FlaskForm
from wtforms import StringField, SubmitField,TextAreaField, DateField, EmailField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo

class BlogForm(FlaskForm):
    title =  StringField("Title", validators=[InputRequired()])
    text = TextAreaField("Text")
    submit = SubmitField("Send")


class SignUp(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(min=10,max=50)],render_kw={"placeholder":"Name"})
    email = EmailField("Email", validators=[InputRequired()],render_kw={"placeholder":"name@email.com"})
    dob = DateField("Date of Birth", validators=[InputRequired()])
    phone_number = StringField("Phone Number", validators=[InputRequired(), Length(min=10,max=10)],render_kw={"placeholder":"Enter phone number without STD code"})
    password = PasswordField("Password",validators=[InputRequired(), Length(min=8,max=12)],render_kw={"placeholder":"Password"})
    submit = SubmitField("Sign Up")

class Login(FlaskForm):
    email = EmailField("Email", validators=[InputRequired()],render_kw={"placeholder":"name@email.com"})
    password = PasswordField("Password",validators=[InputRequired(), Length(min=8,max=12)],render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")
