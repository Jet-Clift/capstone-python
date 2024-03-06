from flask import Flask, render_template, redirect, url_for, session, flash, request
from forms import SampleForm
from model import db, connect_to_db, User, Samps
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "secret"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = crud.get_user_by_username(username)

        if user and user.password == password:
            session["username"] = user.username
            flash(f"Successfully logged in as {user.username}.")
            return redirect("/")  
        else:
            flash("Invalid username or password.")
            return redirect("/login")

    return render_template("login.html")

@app.route("/create_acc.html", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = crud.get_user_by_username(username)
        if existing_user:
            flash("Username already exists. Please choose a different username.")
            return redirect("/create_acc.html")

        new_user = crud.create_user(username, password)
        session["username"] = new_user.username
        flash("Account created successfully. You are now logged in.")

        return redirect("/")

    return render_template("create_acc.html")
    


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)