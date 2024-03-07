from flask import Flask, render_template, redirect, session, flash, request, send_file
from forms import SampleForm
from model import db, connect_to_db, Samps
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

@app.route("/create_acc", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = crud.get_user_by_username(username)
        if existing_user:
            flash("Username already exists. Please choose a different username.")
            return redirect("/create_acc")

        new_user = crud.create_user(username, password)
        session["username"] = new_user.username
        flash("Account created successfully. You are now logged in.")

        return redirect("/")

    return render_template("create_acc.html")
    
@app.route("/samples")
def all_samples():
    samples = crud.get_samples()
    return render_template("all_samples.html")

@app.route("/add_sample", methods=["POST"])
def add_sample():
    sample_form = SampleForm()
    
    if sample_form.validate_on_submit():
        sample_name = sample_form.sample_name.data
        description = sample_form.description.data
        bpm = sample_form.bpm.data
        key = sample_form.key.data
        file_path = sample_form.file_path.data

        new_sample = Samps(sample_name=sample_name, description=description, bpm=bpm, key=key, file_path=file_path)
        db.session.add(new_sample)
        db.session.commit()
        return render_template("upload_sample.html", sample_form=sample_form)
    else:
        flash("Error: Invalid form submission.")
        return render_template("upload_sample.html", sample_form=sample_form)

@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect("/login")
    username = session["username"]
    user = crud.get_user_by_username(username)
    samples = user.samples
    return render_template("profile.html", samples=samples)

@app.route("/sample/<int:sample_id>")
def sample_details(sample_id):
    sample = crud.get_sample_by_id(sample_id)
    
    if sample:
        return render_template("sample_details.html", sample=sample)
    else:
        return render_template("404.html"), 404

def download_sample(sample_id):
    sample = crud.get_sample_by_id(sample_id)
    if sample:
        file_path = sample.file_path
        return send_file(file_path, as_attachment=True)
    else:
        return render_template("404.html"), 404

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)