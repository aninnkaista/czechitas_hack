import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import datetime as dt
import pandas as pd

from helpers import apology, login_required, lookup, usd, current_overview

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
os.environ['API_KEY'] = 'pk_7e6a4e04f9164373ad1aad6d255f6e82'
# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    # function to return shares symbols and numbers for the current user
    groupped_transactions = current_overview(session["user_id"], db)
    # find current price
    groupped_transactions['quote'] = groupped_transactions['shares'].apply(lambda x:
        lookup(x)['price'])
    # calculate total holding value and round it to 2 decimals
    groupped_transactions['total_sum'] = round(
        groupped_transactions['quote'] * 
        groupped_transactions['number'],
        2)
    # flask html does not understand pandas dataframes, so I transfer it to dict of dicts
    transactions = groupped_transactions.to_dict('index')
    # cash remaining from users table
    rem_cash = db.execute("SELECT cash FROM users WHERE id = :user_id",
    user_id = session["user_id"])[0]["cash"]
    return render_template("index.html", transactions = transactions, remaining = round(rem_cash, 2))

@app.route("/change_password", methods = ["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        # check that old password is correct
        old_hash_db = db.execute("SELECT hash from users WHERE id = :user_id",
            user_id = session["user_id"])[0]["hash"]
        if not check_password_hash(old_hash_db, request.form.get("old_password")):
            return apology("invalid current password", 403)
        # check that new password was given
        if not request.form.get("new_password"):
            return apology("must provide new password", 403)      
       # check that repeated password is the same
        if request.form.get("new_password") != request.form.get("new_repeat_password"):
            return apology("new password and repeated password do not match", 403)            
        # update password for the logged in user in the database
        db.execute("UPDATE users SET hash = :hashed_pwd WHERE id = :user_id",
            hashed_pwd = generate_password_hash(request.form.get("new_password")),
            user_id = session["user_id"])
        # to redirect to index page
        return redirect("/")
    elif request.method == "GET":
        return render_template("change_password.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        shares_symbol = request.form.get("symbol")
        # to check if symbol was provided and if prodived symbol does not exist
        if not shares_symbol or not lookup(shares_symbol):
            return apology("Typed in symbol of shares does not exist", 403)
        # to check that the number of shares is integer
        try: 
            int(request.form.get("shares"))
        except ValueError:           
            return apology("Number of shares should be positive integer", 403)
        # and positive integer
        if int(request.form.get("shares")) < 0:
            return apology("Number of shares should be positive integer", 403)
        shares_number = int(request.form.get("shares"))
        info_shares = lookup(shares_symbol)
        cur_price = float(info_shares["price"])
        total_amount = shares_number * cur_price
        # to check the remaining amount of money user has
        session["user_id"]
        cur_amount = float(db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id=session["user_id"])[0]["cash"])
        if cur_amount < total_amount:
            return apology("You don't have enough money to buy given amount of stock", 403)
        else:
            # to update remaining amount in the users table
            new_amount = cur_amount - total_amount
            db.execute("UPDATE users SET cash = :new_amount WHERE id = :user_id",
            new_amount = new_amount, user_id = session["user_id"])
            # to insert row of data into history_purchase table            
            tr_date = dt.datetime.now().strftime("%d-%m-%Y %H:%M")
            db.execute("INSERT INTO history_transactions (user_id, date, purchase, shares, number, price, total_amount) VALUES (?,?,?,?,?,?,?)",
            session["user_id"], str(tr_date), 1, shares_symbol, shares_number, cur_price, total_amount)
            return redirect("/")
    elif request.method == "GET":
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    # to select all transactions for the logged in user
    all_transactions = db.execute("SELECT * FROM history_transactions WHERE user_id = :user_id",
    user_id = session["user_id"])
    transactions_df = pd.DataFrame(all_transactions)    
    transactions_df['type'] = transactions_df['purchase'].map({0: 'sale', 1: 'purchase'})
    # to choose relevant columns
    transactions_df = transactions_df[["date", "type", "shares", "number", "price", "total_amount"]]
    # dict of dicts by index
    transactions = transactions_df.to_dict('index')
    return render_template("history.html", transactions = transactions)


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
    # post method
    if request.method == "POST":
        cur_quote = lookup(request.form.get("symbol"))
        # if quote exists to print it out in a new template
        if cur_quote:
            return render_template("quoted.html", cur_quote = cur_quote)
        # if not error message
        else:
            return apology("Quote was not found", 403)
    # get method
    if request.method == "GET":
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # to check if name was given and if it is unique
        if not request.form.get("username"):
            return apology("No username", 403)
        elif db.execute("SELECT * FROM users WHERE username = :username", 
                username=request.form.get("username")):
            return apology("Username already exist please choose the new one", 403)
        # to check if password was given and if it is the same as repeat password
        if not request.form.get("password"):
            return apology("No password", 403)
        # to check if both password was repeated correctly
        elif request.form.get("repeat_password") != request.form.get("password"):
            return apology("Your password and repeated password are not the same", 403)  
        # to save username and hashed password to the database      
        name = request.form.get("username")
        hash_password = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", name, hash_password)
        return redirect("/login")
    if request.method == "GET":
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        # to check if some symbol was chosen
        if not request.form.get("symbol"):
            apology("No shares were chosen for sale", 403)
        else:
            shares_symbol = request.form.get("symbol")
        # to check that number of shares to sell is number
        try: 
            int(request.form.get("shares"))
        except ValueError:           
            return apology("Number of shares should be positive integer", 403)
        # and positive integer
        if int(request.form.get("shares")) < 0:
            return apology("Number of shares should be positive integer", 403)
        sell_num = int(request.form.get("shares"))
        # to check if user have enough of shares
        # to get numbers of shares from all history transactions 
        # for the logged user and given symbol
        cur_shares = db.execute("SELECT purchase, number FROM history_transactions WHERE user_id = :user_id AND shares =:shares",
            user_id = session["user_id"], shares = shares_symbol)
        cur_shares_df = pd.DataFrame(cur_shares)
        # sales with - sign
        cur_shares_df.loc[cur_shares_df.purchase == 0, "number"] = (-1) * cur_shares_df.loc[cur_shares_df.purchase == 0, "number"]
        # calculate current number of shares owned
        cur_num = cur_shares_df["number"].sum()
        # compare input number to sell with the current stock
        if sell_num > cur_num:
            return apology(f"You own only {cur_num} shares of {shares_symbol}", 403)
        cur_price = float(lookup(shares_symbol)["price"])
        total_amount = float(cur_price * sell_num)
        tr_date = dt.datetime.now()
        # to insert row into history_purchase table            
        tr_date = dt.datetime.now().strftime("%d-%m-%Y %H:%M")
        db.execute("INSERT INTO history_transactions (user_id, date, purchase, shares, number, price, total_amount) VALUES (?,?,?,?,?,?,?)",
        session["user_id"], str(tr_date), 0, shares_symbol, int(sell_num), cur_price, total_amount)
        # to get cash before sale
        cur_amount = float(db.execute("SELECT cash FROM users WHERE id = :user_id",
                    user_id=session["user_id"])[0]["cash"])        
        # to update remaining amount in the users table
        new_amount = cur_amount + total_amount
        db.execute("UPDATE users SET cash = :new_amount WHERE id = :user_id",
        new_amount = round(new_amount, 2), user_id = session["user_id"])
        return redirect("/")

    if request.method == "GET":
        # to get symbols
        symbols = current_overview(session["user_id"], db)['shares'].to_list()
        print(current_overview(session["user_id"], db))
        return render_template("sell.html", symbols = symbols)

    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
