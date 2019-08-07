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
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute("SELECT Symbol, Name, sum(Shares) as Shares, avg(UnitPrice) as UnitPrice, sum(TotalPrice) as TotalPrice "
                            "FROM portfolio WHERE UserId = :uid "
                            "GROUP BY Symbol "
                            "ORDER BY Shares DESC", uid=session.get("user_id"))

    cashWithUser = db.execute("SELECT cash FROM users WHERE id = :uid", uid=session.get("user_id"))
    cash = float(cashWithUser[0]["cash"])
    moneySpent = []
    totalCash = cash
    symbolPrice = {}

    for stock in stocks:
        quote = lookup(stock["Symbol"])
        moneySpent.append(quote["price"] * stock["Shares"])
        symbolPrice[quote["symbol"]] = quote["price"]

    for money in moneySpent:
        totalCash = totalCash + money

    return render_template("index.html", stocks=stocks, cash=cash, totalCash=totalCash, symbolPrice=symbolPrice)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbl = request.form.get("symbol")
        quote = lookup(symbl)
        share = request.form.get("shares")
        row = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session.get("user_id"))
        try:
            int(share)
        except ValueError:
            return apology("Please enter an Integer", 400)

        if not quote:
            return apology("Your symbol was invalid", 400)
        user=session.get("user_id")
        userTotalStockPrice = (float(quote['price']) * float(share))
        cashWithUser = float(row[0]["cash"])

        if not row:
            return apology("user not found", 400)
        if symbl == "" or share == "":
            return apology("You did not enter the symbol, or,s the amount of shares you wanted.", 400)
        if float(share) % 1 != 0 or float(share) <= 0:
            return apology("share has to be positive and non-negative", 400)
        if cashWithUser >= userTotalStockPrice:
            successfulPurchase = db.execute("INSERT INTO portfolio (UserId, Symbol, Name, Shares, UnitPrice, TotalPrice, Time) "
                                            "VALUES(:userid, :symbol, :name, :shares, :price, :total, :time)",
                                            userid=user, symbol=symbl, name=quote['name'], shares=share, price=quote['price'],
                                            total=userTotalStockPrice, time=datetime.datetime.now())
            insertToHistory = db.execute("INSERT INTO history (Symbol, Shares, Price, Transacted, UserId) "
                                            "VALUES(:sym, :shrs, :prce, :date, :uid)",
                                            sym=symbl, shrs=share, prce=float(quote["price"]), date=datetime.datetime.now(), uid=user)
            if not insertToHistory:
                return apology("Could not record transaction", 400)
            if not successfulPurchase:
                return apology("Unsuccessful Purchase", 400)
            cashUpdated = db.execute("UPDATE users SET cash = cash - :userPrice WHERE id = :userId", userId=user, userPrice=userTotalStockPrice)

            if not cashUpdated:
                return apology("Account Update Failed", 400)
        else:
            return apology("You dont have enough moolah")

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * FROM history WHERE UserId = :uid", uid=session.get("user_id"))
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
        symbl = request.form.get("symbol")
        quote = lookup(symbl)
        if not quote or symbl == "":
            return apology("Either your symbol was invalid or was not entered", 400)
        else:
            return render_template("quoted.html", name=quote['name'], symbl=request.form.get("symbol"), price=quote['price'])
    else:
        return render_template("quote.html")


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



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        shares = request.form.get("shares")
        symbl = request.form.get("symbol")
        sharesWithUser = db.execute("SELECT Symbol, Name, sum(Shares) as Shares, avg(UnitPrice) as UnitPrice, sum(TotalPrice) as TotalPrice "
                            "FROM portfolio WHERE UserId = :uid and Symbol = :symbol "
                            "GROUP BY Symbol ", uid=session.get("user_id"), symbol=symbl)
        quote = lookup(symbl)

        if symbl == "" or shares == "":
            return apology("you did not enter one of the fields", 400)

        if not sharesWithUser:
            return apology("failed to receive your shares", 400)

        if symbl == "":
            return apology("You did not enter a Symbol", 400)
        else:
            if int(shares) == 0:
                insertToHistory = db.execute("INSERT INTO history (Symbol, Shares, Price, Transacted, UserId) "
                                            "VALUES(:sym, :shrs, :prce, :date, :uid)",
                                            sym=symbl, shrs=int(shares), prce=float(quote["price"]), date=datetime.datetime.now(), uid=session.get("user_id"))
                if not insertToHistory:
                    return apology("Could not record transaction", 400)
                    return redirect("/")
            if int(shares) > int(sharesWithUser[0]['Shares']):
                return apology("You are trying to sell more stocks than you have", 400)
            if int(shares) == int(sharesWithUser[0]['Shares']):
                cashWithUser = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session.get("user_id"))
                quote = lookup(symbl)
                cash = (float(quote["price"]) * int(shares)) + cashWithUser[0]["cash"]
                delete = db.execute("DELETE FROM portfolio WHERE Symbol = :symbol and UserId = :uid", symbol=symbl, uid=session.get("user_id"))

                if not delete:
                    return apology("Failed to Sell", 400)

                addCashBack = db.execute("UPDATE users SET cash = :cashToAddBack WHERE id = :uid", cashToAddBack=cash, uid=session.get("user_id"))

                insertToHistory = db.execute("INSERT INTO history (Symbol, Shares, Price, Transacted, UserId) "
                                            "VALUES(:sym, :shrs, :prce, :date, :uid)",
                                            sym=symbl, shrs=int(shares)*-1, prce=float(quote["price"]), date=datetime.datetime.now(), uid=session.get("user_id"))
                if not insertToHistory:
                    return apology("Could not record transaction", 400)

                return redirect("/")
            if int(shares) < int(sharesWithUser[0]['Shares']):

                cashWithUser = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session.get("user_id"))

                sharesWithUser = db.execute("SELECT Symbol, Name, sum(Shares) as Shares, avg(UnitPrice) as UnitPrice, sum(TotalPrice) as TotalPrice "
                            "FROM portfolio WHERE UserId = :uid and Symbol = :symbol "
                            "GROUP BY Symbol ", uid=session.get("user_id"), symbol=symbl)

                cash = float(quote["price"]) * (int(sharesWithUser[0]["Shares"]) - int(shares)) + float(cashWithUser[0]["cash"])

                insertToHistory = db.execute("INSERT INTO history (Symbol, Shares, Price, Transacted, UserId) "
                                            "VALUES(:sym, :shrs, :prce, :date, :uid)",
                                            sym=symbl, shrs=int(shares)*-1, prce=float(quote["price"]), date=datetime.datetime.now(), uid=session.get("user_id"))
                sharesLeft = int(sharesWithUser[0]['Shares'])-int(shares)
                if not insertToHistory:
                    return apology("Could not record transaction", 400)

                deleted = db.execute("DELETE FROM portfolio WHERE Symbol = :symbol and UserId = :uid", symbol=symbl, uid=session.get("user_id"))
                if not deleted:
                    return apology("Could not update your stocks", 400)

                insertBackToPortfolio = db.execute("INSERT INTO portfolio (UserId, Symbol, Name, Shares, UnitPrice, TotalPrice, Time) "
                                                   "VALUES(:userid, :symbol, :name, :shares, :price, :total, :time)",
                                                   userid=session.get("user_id"), symbol=symbl, name=quote['name'], shares=sharesLeft, price=quote['price'],
                                                   total=quote['price']*sharesLeft, time=datetime.datetime.now())
                if not insertBackToPortfolio:
                    return apology("Could not complete your transaction", 400)

                cash = (float(quote["price"]) * int(shares)) + cashWithUser[0]["cash"]
                changeUserCash = db.execute("UPDATE users SET cash = :updatedCash", updatedCash=cash)
                return redirect("/")
    else:
        stocks = db.execute("SELECT Symbol FROM portfolio WHERE UserId = :uid GROUP BY Symbol", uid=session.get("user_id"))
        return render_template("sell.html", stocks=stocks)

    return redirect("/")

@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    if request.method == "POST":
        passChanged = False
        passOne = request.form.get("passwordOne")
        passTwo = request.form.get("passwordTwo")

        if passOne == "" or passTwo == "":
            passChanged = False
            return apology("You did not enter one of the fields", 400)

        if str(passOne) != str(passTwo):
            passChanged = False
            return apology("Your passwords were not the same. Try Again", 400)

        if str(passOne) == str(passTwo):
            pwd_hash = generate_password_hash(passOne)
            updatedPassword = db.execute("UPDATE users SET hash = :newPasswordHash WHERE id = :uid", newPasswordHash=pwd_hash, uid=session.get("user_id"))

            if not updatedPassword:
                passChanged = False
                return apology("Password change failed", 400)
            else:
                passChanged = True
                return render_template("changed.html", passChanged=passChanged)

    else:
        return render_template("password.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
