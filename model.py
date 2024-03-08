"""Models for the samples library"""

import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """The user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"
    
class Samps(db.Model):
    """The samples."""
    __tablename__ = "samps"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sample_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    bpm = db.Column(db.Integer, nullable=False)
    key = db.Column(db.String(25), nullable=False)
    file_path = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    
    user = db.relationship("User", backref="samples", lazy=False)

    def __repr__(self):
        return f"<Samps id={self.id} sample name={self.sample_name}>"



def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("connected to db!")