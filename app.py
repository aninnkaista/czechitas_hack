from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from help_functions import apology

import sqlite3

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure database


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use signed cookies
app.secret_key = "546546541534165341"

@app.route("/", methods=["GET"])
def index():
    diary_records = []
    return render_template("dashboard.html", diary_records = diary_records)

@app.route("/new_form", methods=["GET", "POST"])
def new_form():
    if request.method == "POST":
        new_record = []
        return redirect("/")
    elif request.method == "GET":
        return render_template("form.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

