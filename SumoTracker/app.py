import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """  Homepage interface """
    return render_template("index.html")


@app.route("/school_tracker")
@login_required
def school_tracker():
    """render school_tracker.html"""
    return render_template("school_tracker.html")


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash("You are Successfully logged in")

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


@app.route("/signup", methods=["GET", "POST"])
@login_required
def signup():
    """sign up daily newsletter."""
    if request.method == "POST":
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        email = request.form.get("email")
        company_name = request.form.get("company")
        user_id = session["user_id"]


        if not first_name:
            return apology("Please Type Your First Name!")
        elif not last_name:
            return apology("Please Type Your Last Name!")
        elif not email:
            return apology("Please Type Your Email!")
        elif not company_name:
            return apology("Please Type Your Company Name!")

        db.execute("INSERT INTO newsletter (first_name, last_name, company_name, Email, user_id) VALUES(?, ?, ?, ?, ?)", first_name, last_name, company_name, email, user_id)

        flash("You are successfully signed up for our weekly newsletters!")
        return redirect("/")
    else:
        return render_template("form.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Please Input Your Username First!")
        elif not password:
            return apology("Please Input Your Password!")
        elif not confirmation:
            return apology("Please Confirm Your Password First!")
        if password != confirmation:
            return apology("Your Password Doesn't Match!")

        hash = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            return redirect("/")
        except:
            return apology("Username has already been taken!")

    else:
        return render_template("register.html")


@app.route("/news")
@login_required
def news():
    """let's be updated with some news!"""
    return render_template("news.html")



@app.route("/research")
@login_required
def research():
    return render_template("research.html")



@app.route("/blog")
@login_required
def blog():
    return render_template("blog.html")



@app.route("/aboutus")
@login_required
def aboutus():
    return render_template("about.html")



@app.route("/community_event")
@login_required
def community_event():
    return render_template("community.html")
