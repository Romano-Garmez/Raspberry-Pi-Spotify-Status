from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import os


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

CLIENT_ID = "a5a6689bc6f848a8a4a52d732e0de113"
CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login-success")
def login_success():
    access_code = request.form.get("access_token")

    #session["access_token"] = access_token
    return render_template("login-success.html")
