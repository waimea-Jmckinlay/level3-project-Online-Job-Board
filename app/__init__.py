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
# home page
# -----------------------------------------------------------
@app.get("/")
def return_user():  
    with connect_db() as db:
        # Assume user not logged in
        user_id = None
        jobs = None
        offers = None
        
        # Try to get user info
        user_info = session.get("user")
        if user_info != None:
            user_id = session.get("user").get("id")

        # If successful, get the user's jobs
        if user_id != None:
            sql = """
                SELECT id, title, notes, due_by_date, address, user_id
                FROM jobs 
                WHERE user_id = ?
            """
            params = (user_id,)
            jobs = db.execute(sql, params).fetchall()

            sql = """
                SELECT offers.id, offers.jobs_id, offers.users_id, offers.accpeted, jobs.id
                FROM offers 
                WHERE offers.users_id = ?
                RIGHT JOIN jobs ON offers.jobs_id = jobs.id
            """
            params = (user_id,)
            offers = db.execute(sql, params).fetchall()


        else:
            sql = """
                SELECT id, title, notes, due_by_date, address, user_id
                FROM jobs
               
            """
            params = ()
            jobs = db.execute(sql, params).fetchall()

        return render_template("pages/homepage.jinja", jobs=jobs, offers = offers )
    
#---------------------------------------------------------------
#make job page
#---------------------------------------------------------------
@app.get("/job/new")
def show_job_form():
    return render_template("pages/make_job_page.jinja")

#------------------------------------------------------------
# handle make job page
#------------------------------------------------------------
@app.post("/job")
@login_required
def process_new_job():
    
    title = request.form.get("title", "").strip()
    notes = request.form.get("notes", "").strip()
    due_by_date = request.form.get("due_by_date", "").strip().lower()
    address = request.form.get("address", "").strip()
    user_id = session["user"]["id"]

    with connect_db() as db:

            sql = """
                INSERT INTO jobs (title, notes, due_by_date, address, user_id)
                VALUES (?, ?, ?, ?, ?)
                 """ 
            params = (title, notes, due_by_date, address, user_id,)
            jobs = db.execute(sql, params).fetchall()

            flash("Job created", "success")   
            
            sql = """
                SELECT id, title, notes, due_by_date, address, user_id
                FROM jobs 
                WHERE user_id = ?
            """
            params = (user_id,)
            jobs = db.execute(sql, params).fetchall()

    return render_template("pages/homepage.jinja", jobs=jobs)

# -----------------------------------------------------------
# seach page
# -----------------------------------------------------------
@app.get("/find_job")
@login_required
def find_job():  
    with connect_db() as db:

        user_info = session.get("user")
        if user_info != None:
            user_id = session.get("user").get("id")
         
        if user_id != None:
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
@app.get("/user/new")
def show_signup_form():
    return render_template("pages/sign_up.jinja")

# -----------------------------------------------------------
# Handle user signup
# -----------------------------------------------------------
@app.post("/user")
def process_new_user():
    username = request.form.get("username", "").strip()
    real_name = request.form.get("real_name", "").strip()
    password_hash = request.form.get("password", "").strip().lower()
    contact_info= request.form.get("contact_info", "").strip()
    admin = "0"

    with connect_db() as db:
        sql = "SELECT id FROM users WHERE username=?"
        params = (username,)
        user = db.execute(sql, params).fetchone()

        if user:
            flash(f"username '{username}' already exists", "error")
            return redirect("/user/new")

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
        session["user"] = {
            "id": new_id,
            "username": username,
            "real_name": real_name,
            "contact_info": contact_info,
            "admin": admin,
        }
        
        return redirect("/")

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
        user = db.execute(sql, params).fetchone()

        if not user:
            flash(f"Unknown user", "error")
            return redirect("/login")

        if not check_password_hash(user["password_hash"], password):
            flash(f"Incorrect password", "error")
            return redirect("/login")

        session["logged_in"] = True
        session["user"] = {
           "id":       user["id"],
            "username": user["username"],
            "real_name": user["real_name"],
            "contact_info": user["contact_info"],
            "admin": user["admin"],

        }

        flash("Login successful", "success")

        return redirect("/")
#---------------------------------------------------------------
# logout 
#---------------------------------------------------------------    
@app.get("/logout")
@login_required
def logout_user():
    session.clear()
    flash(f"You have been logged out", "success")
    return redirect("/")


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
            INSERT INTO offers(jobs_id, users_id)
            VALUES (?, ?)
        """
        users_id = session["user"]["id"]
        job_id = id
        params = (job_id, users_id)
        db.execute(sql , params)



        flash("job deleted", "success")    
    return redirect ("/find_job",) 



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

