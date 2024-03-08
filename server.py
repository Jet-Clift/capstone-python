import os
import shutil
from flask import Flask, render_template, redirect, session, flash, request, send_file
from forms import SampleForm
from model import db, connect_to_db, Samps
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = "secret"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/nav")
def navpage():
    return render_template("nav.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = crud.get_user_by_username(username)

        if user and user.password == password:
            session["username"] = user.id
            flash(f"Successfully logged in as {user.username}.")
            return redirect("/nav")  
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
        session["username"] = new_user.id
        flash("Account created successfully.")

        return redirect("/")

    return render_template("create_acc.html")
    
@app.route("/samples")
def all_samples():
    samples = crud.get_samples()
    return render_template("all_samples.html", samples=samples)

@app.route("/add_sample", methods=["GET", "POST"])
def add_sample():
    if request.method == "GET":
        sample_form = SampleForm()
        return render_template("upload_sample.html", sample_form=sample_form)
    elif request.method == "POST":
        if 'file_path' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file_path']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filename = (file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            sample_form = SampleForm(request.form)
            if sample_form.validate_on_submit():
                sample_name = sample_form.sample_name.data
                description = sample_form.description.data
                bpm = sample_form.bpm.data
                key = sample_form.key.data
                file_path = filename
                new_sample = Samps(sample_name=sample_name, description=description, bpm=bpm, key=key, file_path=file_path, user_id=session["username"])
                db.session.add(new_sample)
                db.session.commit()
                return redirect("/samples")
            else:
                flash("Error: Invalid form submission.")
                return render_template("upload_sample.html", sample_form=sample_form)
            
@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect("/login")
    username = session["username"]
    user = crud.get_user_by_id(username)
    samples = user.samples
    return render_template("profile.html", samples=samples)

@app.route("/samples/<int:sample_id>")
def sample_details(sample_id):
    sample = crud.get_sample_by_id(sample_id)
    
    if sample:
        return render_template("sample.html", sample=sample)
    else:
        return render_template("404.html"), 404

@app.route("/samples/<int:sample_id>/download")
def download_sample(sample_id):
    sample = crud.get_sample_by_id(sample_id)
    if sample:
        file_path = sample.file_path
        print(sample.file_path)
        if file_path:

            return send_file(f"C:/Users/xekee/devmountain-work/Capper-part2/uploads/{file_path}", as_attachment=True, mimetype=None)
    else:
        flash("The sample doesn't exist.")
        return redirect("/samples")
    

    
@app.route("/users")
def get_all_users():
    users = crud.get_users()
    print(users)
    return render_template("all_users.html", users=users)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    
    file = request.files["file"]

    if file.filename == "":
        flash("No selected file")
        return redirect("/add_sample")
    
    if file:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        # shutil.move(file_path, os.path.join(app.config["UPLOAD_FOLDER"], "new_filename.wav"))
        flash("File uploaded successfully!", "success")
        return redirect("/samples") 

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)