import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    userDict = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
    username = userDict[0].get("username")
    balancesDict = db.execute("SELECT * FROM balances WHERE username = :username", username=username)
    balancesCount = len(balancesDict)
    # update stock quotes for balances display
    grandTotal = 0
    for i in range(0, balancesCount):
        shares = balancesDict[i].get("shares")
        symbol = balancesDict[i].get("symbol")
        quote = lookup(symbol)
        price = quote["price"]
        total = shares * price
        grandTotal = grandTotal + total
        db.execute("UPDATE balances SET total = :total WHERE symbol = :symbol", total=usd(total), symbol=symbol)
    balancesDict = db.execute("SELECT * FROM balances WHERE username = :username", username=username)
    # get cash balance
    cashDict = db.execute("SELECT cash FROM users WHERE username = :username", username=username)
    availableCash = float(cashDict[0].get('cash'))
    grandTotal = grandTotal + availableCash
    return render_template("/index.html", balancesDict=balancesDict, balancesCount=balancesCount, availableCash=usd(availableCash), grandTotal=usd(grandTotal))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure stock symbol was submitted
        if not request.form.get("stock"):
            return apology("must provide valid stock symbol", 403)
        elif not lookup(request.form.get("stock")):
            return apology("must provide valid stock symbol", 403)
        else:
            stock = request.form.get("stock")

        # Ensure valid number of shares was submitted
        if not request.form.get("shares"):
            return apology("must provide number of shares", 403)
        else:
            shares = int(request.form.get("shares"))

        quote = lookup(stock)
        # name = quote["name"]
        price = quote["price"]
        total = float(shares) * price

        userDict = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
        username = userDict[0].get("username")

        # check cash balance
        cashDict = db.execute("SELECT cash FROM users WHERE username = :username", username=username)
        availableCash = float(cashDict[0].get('cash'))
        if total > availableCash:
             return apology("you don't have enough cash", 403)
        else:
            availableCash = availableCash - total
            db.execute("INSERT INTO history (username, symbol, price, shares, total) VALUES (:username, :symbol, :price, :shares, :total)", username=username, symbol=stock, price=usd(price), shares=shares, total=usd(total))
            db.execute("UPDATE users SET cash = :availableCash", availableCash=availableCash)
            stockDict = db.execute("SELECT * FROM balances WHERE username = :username AND symbol = :stock", username=username, stock=stock)
            if len(stockDict) != 0:
                existingShares = int(stockDict[0].get('shares'))
                shares = shares + existingShares
                total = float(shares) * price
                db.execute("UPDATE balances SET shares = :shares, total = :total WHERE username = :username AND symbol = :stock", username=username, stock=stock, shares=shares, total=usd(total))
            else:
                total = float(shares) * price
                db.execute("INSERT INTO balances (username, symbol, shares, total) VALUES (:username, :symbol, :shares, :total) ", username=username, symbol=stock, shares=shares, total=usd(total))
        return redirect("/")
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    userDict = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
    username = userDict[0].get("username")
    transactions = db.execute("SELECT * FROM history WHERE username=:username", username = username)
    transactionCount = len(transactions)
    return render_template("history.html", transactions=transactions, transactionCount=transactionCount)

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

        username=request.form.get("username")
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # check cash balance
        cashDict = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        availableCash = float(cashDict[0].get('cash'))
        # Redirect user to home page with balances
        balancesDict = db.execute("SELECT * FROM balances WHERE username = :username", username=username)
        balancesCount = len(balancesDict)
        return render_template("/index.html", balancesDict=balancesDict, balancesCount=balancesCount, availableCash=usd(availableCash))
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
# User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure stock symbol was submitted
        if not request.form.get("stock"):
            return apology("must provide stock symbol", 403)
        else:
            # lookup stock
            stock=request.form.get("stock")
            quote = lookup(stock)
            name = quote["name"]
            price = quote["price"]
            symbol = quote["symbol"]
            return render_template("quoted.html", name=name, price=price, symbol=symbol)
    else:
        return render_template("quote.html")




@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        elif not request.form.get("confirmation"):
            return apology("must confimrm password", 403)
        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 403)
        # add user to users table
        username=request.form.get("username")
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash) ", username=username, hash=generate_password_hash(request.form.get("password")))
        # add initial cash to history and balances tables
        db.execute("INSERT INTO history (username, symbol, total) VALUES (:username, :symbol, :total) ", username=username, symbol='CASH', total=10000)
        # db.execute("INSERT INTO balances (username, symbol, total) VALUES (:username, :symbol, :total) ", username=username, symbol='CASH', total=10000)
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
# User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure stock symbol was submitted
        if not request.form.get("stock"):
            return apology("must provide valid stock symbol", 403)
        elif not lookup(request.form.get("stock")):
            return apology("must provide valid stock symbol", 403)
        else:
            stock = request.form.get("stock")

        # Ensure valid number of shares was submitted
        if not request.form.get("shares"):
            return apology("must provide number of shares", 403)
        else:
            shares = int(request.form.get("shares"))

        quote = lookup(stock)
        # name = quote["name"]
        price = quote["price"]


        userDict = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
        username = userDict[0].get("username")

        # check to see whether there is a holding in that stock & then check shares balance
        sharesDict = db.execute("SELECT * FROM balances WHERE username = :username AND symbol = :stock", username=username, stock=stock)
        if len(sharesDict) == 0:
            return apology("no stock in that company", 403)
        else:
            availableShares = float(sharesDict[0].get('shares'))
            if shares > availableShares:
                return apology("you don't have enough shares", 403)
            else:
                # deduct shares
                availableShares = availableShares - shares
                total = float(shares) * price
                db.execute("INSERT INTO history (username, symbol, price, shares, total) VALUES (:username, :symbol, :price, :shares, :total)", username=username, symbol=stock, price=usd(price), shares=shares, total=usd(total))
                # add cash
                cashDict = db.execute("SELECT cash FROM users WHERE username = :username", username=username)
                availableCash = float(cashDict[0].get('cash'))
                availableCash = availableCash + total
                db.execute("UPDATE users SET cash = :availableCash", availableCash=availableCash)
                # update balances
                stockDict = db.execute("SELECT * FROM balances WHERE username = :username AND symbol = :stock", username=username, stock=stock)
                existingShares = int(stockDict[0].get('shares'))
                shares = existingShares - shares
                total = float(shares) * price
                db.execute("UPDATE balances SET shares = :shares, total = :total WHERE username = :username AND symbol = :stock", username=username, stock=stock, shares=shares, total=usd(total))
                return redirect("/")
    else:
        return render_template("sell.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
