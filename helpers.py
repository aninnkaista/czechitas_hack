import os
import requests
import urllib.parse
import pandas as pd

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def current_overview(user_id, db):
    """to get shares symbols and numbers for the given user"""
       # to create a list of dictionaries of stocks owned
    # by the loggedin user
    all_transactions = db.execute("SELECT * FROM history_transactions WHERE user_id = :user_id",
        user_id = user_id)    
    # dataframe from transactions to easier work with data
    transactions_df = pd.DataFrame(all_transactions)
    transactions_df['number'] = pd.to_numeric(transactions_df['number'])
    # group number of shares by shares symbol and purchase bool
    groupped_transactions = transactions_df.groupby(['shares', 'purchase'])['number'
        ].sum().reset_index(level = 'purchase')
    # sale numbers with -
    groupped_transactions.loc[groupped_transactions.purchase == 0, 'number'] = \
        groupped_transactions.loc[groupped_transactions.purchase == 0, 'number'] * (-1)
    # total number of transactions
    groupped_transactions = groupped_transactions.groupby([groupped_transactions.index]
        )['number'].sum().reset_index()
    # to drop rows with total 0 number
    groupped_transactions.drop(index = groupped_transactions[ 
        groupped_transactions.number == 0].index, inplace = True)
    return groupped_transactions