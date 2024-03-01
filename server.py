from flask import Flask, render_template, redirect, url_for, session, flash
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





if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)