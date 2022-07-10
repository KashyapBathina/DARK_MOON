# API KEY
# export API_KEY=pk_63633ff467594e1c8e6823dee78a46a2

import os
from datetime import datetime, timezone
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    """Show portfolio of stocks"""

    owns = own_shares()
    total = 0
    for symbol, shares in owns.items():
        result = lookup(symbol)
        name, price = result["name"], result["price"]
        stock_value = shares * price
        total += stock_value
        owns[symbol] = (name, shares, usd(price), usd(stock_value))
    cash = db.execute("SELECT cash FROM users WHERE id = ? ", session["user_id"])[0]['cash']
    return render_template("index.html", owns=owns, cash=usd(cash), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        if (not request.form.get("symbol")) or (not request.form.get("shares")):
            return apology("must provide stock symbol and number of shares", 403)

        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be a positive integer", 400)

        if shares <= 0:
            return apology("must provide valid number of shares", 400)

        quote = lookup(request.form.get("symbol"))

        if quote == None:
            return apology("stock symbol not valid, please try again")

        cost = int(request.form.get("shares")) * quote['price']

        cash_available = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])

        if cost > cash_available[0]["cash"]:
            return apology("you do not have enough cash for this stock")

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, session["user_id"])

        db.execute("INSERT INTO orders (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], quote["symbol"], int(request.form.get("shares")), quote["price"], time_now())

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    rows = db.execute("SELECT symbol, shares, price, timestamp FROM orders WHERE user_id = ?", session["user_id"])

    if not rows:
        return apology("You have no transactions recorded")

    return render_template("history.html", rows=rows)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Either the stock does not exist or you have provided the incorrect symbol", 400)

        return render_template("quoted.html", name=quote["name"], price=usd(quote["price"]), symbol=quote["symbol"])

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("must fill in all fields", 400)

        elif password != confirmation:
            return apology("passwords must match", 400)

        if len(db.execute('SELECT username FROM users WHERE username = ?', username)) > 0:
            return apology("username already in use", 400)

        result = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))

        session["user_id"] = result

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    owns = own_shares()

    if request.method == "POST":
        if not request.form.get("symbol") or not request.form.get("shares"):
            return apology("you must fill in all fields", 403)

        if owns[request.form.get("symbol")] < int(request.form.get("shares")):
            return apology("you cannot sell more shares than you own", 400)

        result = lookup(request.form.get("symbol"))
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']

        remain = cash + result["price"] * int(request.form.get("shares"))

        db.execute("UPDATE users SET cash = ? WHERE id = ?", remain, session["user_id"])
        db.execute("INSERT INTO orders (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], request.form.get("symbol"), -int(request.form.get("shares")), result["price"], time_now())

        return redirect("/")

    else:
        return render_template("sell.html", owns=owns.keys())


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add money"""
    password = str(4806013822)

    if request.method == "POST":

        if request.form.get("credit") != password:
            return apology("this is an invalid credit card number", 403)

        if int(request.form.get("money")) > int(999):
            return apology("your card declined", 403)

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", request.form.get("money"), session["user_id"])

        return redirect("/")

    else:
        return render_template("add_cash.html")


def time_now():
    # Get current time
    now_utc = datetime.now(timezone.utc)
    return str(now_utc.date()) + ' @time ' + now_utc.time().strftime("%H:%M:%S")


def own_shares():
    owns = {}
    query = db.execute("SELECT symbol, shares FROM orders WHERE user_id = ?", session["user_id"])
    for q in query:
        symbol, shares = q["symbol"], q["shares"]
        owns[symbol] = owns.setdefault(symbol, 0) + shares
    owns = {k: v for k, v in owns.items() if v != 0}
    return owns