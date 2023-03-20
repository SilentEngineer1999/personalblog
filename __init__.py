from flask import Flask, render_template, request, flash, session, abort, redirect, url_for
from forms import BlogForm, SignUp, Login
import secrets
import psycopg2 as sql
from passlib.hash import pbkdf2_sha256
import os
from dotenv import load_dotenv
from datetime import datetime






con = sql.connect(
    database="postgres", user="postgres", 
  password="root", host='db', port='5432'
)

#Create a Connection
cur = con.cursor()


# #Create users table  in db_web database
sql2 = '''CREATE TABLE IF NOT EXISTS users (
	id BIGSERIAL UNIQUE PRIMARY KEY,
	UNAME VARCHAR(50) NOT NULL,
	email VARCHAR(50) NOT NULL,
    phone_number VARCHAR(10) NOT NULL,
	date_of_birth DATE NOT NULL,
    password VARCHAR(200) NOT NULL
);'''

content2 = '''CREATE TABLE IF NOT EXISTS content(
			UNAME VARCHAR(50) NOT NULL,
            email VARCHAR(50) NOT NULL,
            title VARCHAR(50) NOT NULL,
            date DATE NOT NULL,
            text VARCHAR
            );
		'''

cur.execute(sql2)
cur.execute(content2)

#commit changes
con.commit()

#close the connection
con.close()
print("db closed")








# thi is env variables

# DB_NAME = "test"
# DB_USER = "ajays"
# DB_PASSWORD = "9110870379@Ab"
# DB_HOST = "localhost"
# DB_PORT = "5432"

load_dotenv()
app = Flask(__name__)
app.secret_key=secrets.token_urlsafe()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    
    signup_form = SignUp()
    if signup_form.validate_on_submit():
        name = signup_form.name.data
        email = signup_form.email.data
        phonenumber = signup_form.phone_number.data
        dateofbirth = signup_form.dob.data
        password = pbkdf2_sha256.hash(signup_form.password.data)
        con = sql.connect(
    database="postgres", user="postgres", 
  password="root", host='db', port='5432'
)
        con.autocommit = True
        cur = con.cursor()
        cur.execute(f'SELECT * FROM users where email=(%s)',(email,))
        data=cur.fetchall()
        print(data)
        if data:
            flash("User already exists")
            return render_template("signup.html",form=signup_form)
        else:
            cur.execute(f'insert into users (UNAME,email,phone_number,date_of_birth, password) values (%s,%s,%s,%s,%s)',(name,email,phonenumber,dateofbirth,password))
            con.commit()
            con.close()
            flash("Sign Up Successful")
            
    
    login_form = Login()

    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        con = sql.connect(
    database="postgres", user="postgres", 
  password="root", host='db', port='5432'
)

        con.autocommit = True
        cur = con.cursor()
        cur.execute(f'SELECT * FROM users where email=(%s)',(email,))
        data = cur.fetchall()
        print(data)
        if data:
            if email == data[0][2] and pbkdf2_sha256.verify(password, data[0][5]): 
                session["email"] = email
                return redirect(url_for("chatblog"))
        else: 
            flash("Error Incorrect username or password")
            return render_template("login.html", form=login_form, error=True)
    return render_template("login.html", form=login_form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/signup", methods=["GET","POST"])
def sign_up():
    signup_form = SignUp()
    return render_template("signup.html", form=signup_form)

@app.route("/chatblog",methods=["GET","POST"])
def chatblog():
    if not session.get("email"):
        abort(401)
    else:
        con = sql.connect(
    database="postgres", user="postgres", 
  password="root", host='db', port='5432'
)

        con.autocommit = True
        cur = con.cursor()
        cur.execute('select * from users where email=(%s)',(session["email"],))
        data = cur.fetchall()
        print(data)
        uname = data[0][1]
        email = session["email"]
        
        form = BlogForm()
        if request.method=="POST":
            title = form.title.data
            entry = form.text.data
            cur.execute('insert into content (UNAME,email,title, date,text) values (%s,%s,%s,%s,%s)',(uname, email,title, datetime.today().strftime("%Y-%m-%d"), entry))
        
        cur.execute('select * from content where email=(%s)',(session["email"],))
        data = cur.fetchall()
        print(data)
        entries_with_date = [
                (   
                    entry[2],
                    entry[3],
                    entry[4],
                    entry[0]
                )
                for entry in data
            ]
        return render_template("chatblog.html", form=form, name = uname, entries = entries_with_date)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"),404

@app.errorhandler(401)
def page_not_found(error):
    return render_template("401.html"),401 
