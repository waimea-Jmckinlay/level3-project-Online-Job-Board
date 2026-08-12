#===========================================================
# PROJECT NAME HERE
# By YOUR NAME HERE
#===========================================================

from flask import Flask, request, session, render_template, flash, redirect, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
import html
from app.helpers import *


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================

# -----------------------------------------------------------
# Signup page
# -----------------------------------------------------------
@app.get("/home")
def return_user():
    return render_template("pages/homepage.jinja")

# -----------------------------------------------------------
# Signup page
# -----------------------------------------------------------
@app.get("/users/new")
def show_signup_form():
    return render_template("pages/sign_up.jinja")

# -----------------------------------------------------------
# Handle user signup
# -----------------------------------------------------------
@app.post("/users")
def process_new_user():
    username = request.form.get("username", "").strip()
    real_name = request.form.get("real_name", "").strip()
    password_hash = request.form.get("password", "").strip().lower()
    contact_info= request.form.get("contact_info", "").strip()

    with connect_db() as db:
        sql = "SELECT id FROM users WHERE username=?"
        params = (username,)
        users = db.execute(sql, params).fetchone()

        if users:
            flash(f"username '{username}' already exists", "error")
            return redirect("/users/new")

        pass_hash = generate_password_hash(password_hash)

        sql = """
            INSERT INTO users (username, real_name, password_hash, contact_info)
            VALUES (?, ?, ?, ?)
        """



        params = (username, real_name, pass_hash, contact_info)
        db.execute(sql, params)

        session["logged_in"] = True
        session["users"] = {
            "id":       users["id"],
            "username": users["username"],
            "real_name": users["real_name"],
            "contact_info": users["contact_info"],
            "password_hash":  users["password_hash"],
            "admin": users["admin"],
            "rating": users["rating"]
        }
        flash("Account created", "success")
        return redirect("/home")

# -----------------------------------------------------------
# login page
# -----------------------------------------------------------
@app.get("/login")
def show_login_form():
    return render_template("pages/login.jinja")

#------------------------------------------------------------
#login form
#------------------------------------------------------------


@app.post("/login")
def process_user_login():
    username = request.form.get("username", "").strip().lower()
    password = request.form.get("password_hash", "").strip()

    with connect_db() as db:
        sql = """
            SELECT id, username, real_name,  contact_info, password_hash, admin, rating
            FROM users 
            WHERE username = ?
        """
        params = (username,)
        users = db.execute(sql, params).fetchone()

        if not users:
            flash(f"Unknown user", "error")
            return redirect("/login")

        if not check_password_hash(users["password_hash"], password):
            flash(f"Incorrect password", "error")
            return redirect("/login")

        session["logged_in"] = True
        session["users"] = {
           "id":       users["id"],
            "username": users["username"],
            "real_name": users["real_name"],
            "contact_info": users["contact_info"],
            "password_hash":  users["password_hash"],
            "admin": users["admin"],
            "rating": users["rating"]
        }

        flash("Login successful", "success")

        return redirect("/home")





#-----------------------------------------------------------
# Home page - Show all jobs
#-----------------------------------------------------------
@app.get("/")
def show_jobs():
    with connect_db() as db:
        sql = """
            SELECT id, title, notes, due_by_date, address, user_id
            FROM jobs
        """
        params = ()
        jobs = db.execute(sql, params).fetchall()

        flash("Test message")
        flash("Test SUCCESS message", "success")
        flash("Test INFO message", "info")
        flash("Test WARNING message", "warning")
        flash("Test ERROR message", "error")

        return render_template("pages/jobs_list.jinja", jobs=jobs)


#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)

