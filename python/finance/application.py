import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Ensure environment variable is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

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
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Query user's portfolio from db
    portfolio = db.execute(
        "SELECT symbol, SUM(shares) as number_of_shares, price FROM transactions WHERE user_id = :user_id GROUP BY symbol", user_id=session["user_id"])

    # Query database for cash
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

    # Check available cash
    cash_available = cash[0]["cash"]

    return render_template("index.html", portfolio=portfolio, cash_available=cash_available)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        # Get quote
        stock = lookup(request.form.get("symbol"))

        # Check if ticker is valid
        if stock == None:
            return apology("No ticker found")

        # Check the amount of shares user wants to buy
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Must be a number")

        # Check if the user choose a positive amount
        if shares < 0:
            return apology("Must be a positive number")

        # Query database for cash
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id=session["user_id"])

        # Get cash available
        cash_available = cash[0]["cash"]

        # Check stock's current price
        price = stock["price"]

        # Output total price of the sell
        total = shares * price

        # Check users' balance
        if cash_available < total:
            return apology("Not enough cash")

        # Submit buy order to database and update cash balance
        db.execute("UPDATE users SET cash = cash - :total WHERE id = :user_id", total=total, user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"], symbol=request.form.get("symbol"), shares=shares, price=price)

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Check user's order history
    history = db.execute("SELECT * FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])

    return render_template("history.html", history=history)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        # Get quote information
        stock = lookup(request.form.get("symbol"))

        # Check if ticker is valid
        if stock == None:
            return apology("No ticker found")

        return render_template("quoted.html", stock=stock)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reach route via POST
    if request.method == "POST":

        # Check that user inputs a username
        if not request.form.get("username"):
            return apology("Must provide username")

        # Check that user inputs a password
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("Must provide password")

        # Ensure that user inputs the password two times
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords doesn't match")

        # Hash the password using generate_password_hash
        hash = generate_password_hash(request.form.get("password"))

        # Submit username and password to database
        submit = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                            username=request.form.get("username"), hash=hash)

        if not submit:
            return apology("Username already exist")
        else:
            return apology("Registration complete!", 200)

        # Remember which user has logged in
        session["user_id"] = submit

        # Redirect user to login page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/topup", methods=["GET", "POST"])
@login_required
def add_cash():
    """ PERSONAL TOUCH:
    Let's the user add cash to their balance
    """

    # Query database for cash
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

    # Check account balance
    cash_available = cash[0]["cash"]

    if request.method == "POST":

        # Get user input (allow floats)
        try:
            topup = float(request.form.get("cash"))
        except:
            return apology("Must be a number")

        # Check if the user choose a positive amount
        if topup < 0:
            return apology("Must be a positive number")

        # Update users cash balance
        db.execute("UPDATE users SET cash = cash + :topup WHERE id = :user_id", user_id=session["user_id"], topup=topup)

        # Redirect to home page
        return redirect("/")

    else:
        return render_template("topup.html", cash_available=cash_available)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        # Get quote
        stock = lookup(request.form.get("symbol"))

        # Check if ticker is valid
        if stock == None:
            return apology("No ticker found")

        # Check the amount of shares user wants to buy
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Must be a number")

        # Check if the user choose a positive amount
        if shares < 0:
            return apology("Must be a positive number")

        # Check user's available shares
        available_shares = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id and symbol = :symbol GROUP BY symbol",
                                      user_id=session["user_id"], symbol=request.form.get("symbol"))

        # If user have the sellable shares
        if available_shares[0]["total_shares"] < 1 or shares > available_shares[0]["total_shares"]:
            return apology("You don't have enough shares")

        # Check stock's current price
        price = stock["price"]

        # Output total price of the purchase
        total = shares * price

        # Submit sell order to database and update cash balance
        db.execute("UPDATE users SET cash = cash + :total WHERE id = :user_id", user_id=session["user_id"], total=total)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                   user_id=session["user_id"], symbol=request.form.get("symbol"), shares=-shares, price=price)

        return redirect("/")

    else:
        available_shares = db.execute(
            "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol", user_id=session["user_id"])
        return render_template("sell.html", available_shares=available_shares)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
