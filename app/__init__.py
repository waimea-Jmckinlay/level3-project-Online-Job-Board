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
# once signed up 
# -----------------------------------------------------------
@app.get("/home")
@login_required
def return_user():  
    with connect_db() as db:
        sql = """
            SELECT id, title, notes, due_by_date, address, user_id
            FROM jobs 
            WHERE user_id = id
        """
        params = ()
        jobs = db.execute(sql, params).fetchall()


        return render_template("pages/homepage.jinja", jobs=jobs)

# -----------------------------------------------------------
# seach page
# -----------------------------------------------------------
@app.get("/find_job")
@login_required
def find_job():  
    with connect_db() as db:
        sql = """
            SELECT id, title, notes, due_by_date, address, user_id
            FROM jobs
        """
        params = ()
        jobs = db.execute(sql, params).fetchall()


        return render_template("pages/search_page.jinja", jobs=jobs)


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
    admin = request.form.get("admin","")

    with connect_db() as db:
        sql = "SELECT id FROM users WHERE username=?"
        params = (username,)
        users = db.execute(sql, params).fetchone()

        if users:
            flash(f"username '{username}' already exists", "error")
            return redirect("/users/new")

        pass_hash = generate_password_hash(password_hash)

        sql = """
            INSERT INTO users (username, real_name, password_hash, contact_info, admin)
            VALUES (?, ?, ?, ?, ?)
        """ 

        params = (username, real_name, pass_hash, contact_info, admin)
        result = db.execute(sql, params)

        flash("Account created", "success")
        
        # Get the ID of the new username
        new_id = result.lastrowid

        session["logged_in"] = True
        session["users"] = {
            "id": new_id,
            "username": username,
            "real_name": real_name,
            "contact_info": contact_info,
            "admin": admin
        }
        
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
    password = request.form.get("password", "").strip()

    with connect_db() as db:
        sql = """
            SELECT id, username, real_name,  contact_info, password_hash, admin
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
        session["user"] = {
           "id":       users["id"],
            "username": users["username"],
            "real_name": users["real_name"],
            "contact_info": users["contact_info"],
            "admin": users["admin"],
            # "rating": users["rating"]
        }

        flash("Login successful", "success")

        return redirect("/home")
#---------------------------------------------------------------
# logout 
#---------------------------------------------------------------    
@app.get("/logout")
@login_required
def logout_user():
    session.clear()
    flash(f"You have been logged out", "success")
    return redirect("/")


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
#----------------------------------------------------------------------------
#job-delete
#----------------------------------------------------------------------------------
@app.get(f"/job/<int:id>/delete")
@login_required
def process_delete_job(id):
    with connect_db() as db:
        sql = """
            SELECT user_id FROM jobs WHERE id=?
        """
        params = (id,)
        jobs = db.execute(sql, params).fetchone()
        users = db.execute(sql, params).fetchone()

        if jobs and users ["user_id"] == session["user"]["id"]:

            sql = """
                DELETE FROM jobs WHERE id=?
            """
            params = (id,)
            db.execute(sql, params)

            flash("job deleted", "success")
            return redirect("/find_job")

        flash("Invalid job", "error")
        return redirect("/find_job")
#--------------------------------------------------------------
#accapted jobs funchtion 
#--------------------------------------------------------------
@app.get("/job/<int:id>/accept")
@login_required
def process_accept_job(id):  
    with connect_db() as db:
        sql = """
            SELECT job_id, user_id
            FROM offers 
            WHERE job_id=? AND user_id=?
        """
        user_id = session["user"]["id"]
        params = (id, user_id)
        offers = db.execute(sql , params).fetchone()



    
    return redirect ("/find_job") 



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

