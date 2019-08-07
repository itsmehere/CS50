import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///passwords.db")


@app.route("/")
@login_required
def credentials():
    """Show all registered applications"""

    rows = db.execute("SELECT * FROM password WHERE UserId = :uid",
                      uid=session.get("user_id"))

    if not rows:
        return render_template("norows.html")
    else:
        return render_template("credentials.html", rows=rows)

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Show specific applications"""
    if request.method == "POST":
        web = request.form.get("website")

        if not web or web == "":
            return apology("Try again.")

        web = web + '%'
        rows = db.execute("SELECT * FROM password WHERE UserId = :uid and website LIKE :webs", uid=session.get("user_id"), webs=web)

        if not rows:
            return render_template("norows.html")
        else:
            return render_template("credentials.html", rows=rows)
    else:
        return render_template("search.html")

@app.route("/addpasswords", methods=["GET", "POST"])
@login_required
def addPassword():
    """add a password"""
    if request.method == "POST":
        web = request.form.get("website")
        password = request.form.get("pass")
        username = request.form.get("user")

        if web == "" or password == "" or username == "":
            return apology("One of the fields was empty")
        if not web or not password or not username:
            return apology("Invlaid Input")

        user = session.get("user_id")

        successfulAddition = db.execute("INSERT INTO password (UserId, website, username, password) "
                                            "VALUES(:userid, :website, :uname, :passwordForSite)",
                                            userid=user, website=web, uname=username, passwordForSite=password)
        if not successfulAddition:
            return apology("There was an error")
        else:
            return render_template("success.html")
    else:
        return render_template("passwords.html")

@app.route("/deletepasswords", methods=["GET", "POST"])
@login_required
def deletePassword():
    """delete a password"""
    if request.method == "POST":
        web = request.form.get("website")

        if not web:
            return apology("Error")

        user = session.get("user_id")

        successfulDeletion = db.execute("DELETE FROM password WHERE UserId = :uid and website = :webs",
                                        uid=session.get("user_id"), webs=web)

        if not successfulDeletion:
            return apology("ERROR NO PASSWORDS TO DELETE")
        else:
            return render_template("success.html")
    else:
        return render_template("dpasswords.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username=request.form.get("username")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("the passwords must match", 400)

        pwd_hash = generate_password_hash(request.form.get("password"))

        # Query database for username
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES(:uname, :password_hash)",
                                    uname=username, password_hash=pwd_hash)

         # unique username constraint violated?
        if not new_user_id:
            return apology("username taken", 400)

        # Remember which user has logged in
        session["user_id"] = new_user_id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
