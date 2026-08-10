#============================================================================
# Database schema and seed data configuration
#============================================================================


#----------------------------------------------------------------------------
# Table definitions
#----------------------------------------------------------------------------
# Define your tables with a name, a schema and optional seed/sample data,
# using this format, and then add the tables to the Table Registry below:
#
# class TableName:
#     NAME      = "name"
#     SCHEMA    = "CREATE TABLE name (...)"
#     SEED_DATA = "INSERT INTO name (...)" or None
#----------------------------------------------------------------------------

class UserTable:

    NAME = "users"

    SCHEMA = """
        CREATE TABLE users (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
           username TEXT NOT NULL,
           real_name TEXT NOT NULL,
           password_hash TEXT NOT NULL,
           contact_info TEXT,
           admin INTEGER,
           rating TEXT
        )
    """

    SEED_DATA = """
        INSERT INTO users (username, real_name, password_hash, contact_info, admin, rating )
        VALUES            ("bob",  "sam", " scrypt:32768:8:1$n7eJTucLbaGmUpAM$c1776374a8d456a6eaf61bccc08db5e1fcc4ff3b3983d364c45ab13074255eeae0a393afb11f99a9fe63fb1d980992ace17a72ba70324523b11e92e36cbe4252", "phone number 54873657893", "0", "do not recamend "),
                          ("ham",  "damm", " scrypt:32768:8:1$n7eJTucLbaGmUpAM$c1776374a8d456a6eaf61bccc08db5e1fcc4ff3b3983d364c45ab13074255eeae0a393afb11f99a9fe63fb1d980992ace17a72ba70324523b11e92e36cbe4252", "phone number 54873657893", "0", " will recamend ")
               

    """

class JobTable:

    NAME = "jobs"

    SCHEMA = """
        CREATE TABLE jobs (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
           title TEXT NOT NULL,
           notes TEXT NOT NULL,
           due_by_date TEXT NOT NULL,
           address TEXT NOT NULL,
           user_id INTEGER NOT NULL,

           FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """

    SEED_DATA = """
        INSERT INTO jobs (title, notes, due_by_date, address, user_id)
        VALUES ("Welcome!", "repear my roof" , "5/7/2029", "5th YUMMY", "1")


    """

class OffersTable:

    NAME = "offers"

    SCHEMA = """
        CREATE TABLE offers (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
           job_id INTEGER NOT NULL,
           user_id INTEGER NOT NULL,
           accpeted INTEGER NOT NULL,
           job_done INTEGER NOT NULL,

           FOREIGN KEY (job_id) REFERENCES jobs (id),
           FOREIGN KEY (user_id)  REFERENCES user (id)
        )
    """

    SEED_DATA = """
        INSERT INTO offers (job_id, user_id, accpeted, job_done)
        VALUES ("1","2","1","0" )

    """




#----------------------------------------------------------------------------
# Table registry
#----------------------------------------------------------------------------
# Register all of your tables by adding them to the TABLES list here:
#
# TABLES = [
#     Table1Name,
#     Table2Name,
#     etc.
# ]
#
# Note: The table order is important - Create the tables that have
# foreign keys *after* the tables they link to have been created
#----------------------------------------------------------------------------

TABLES = [
    UserTable,
    JobTable,
    OffersTable
]

