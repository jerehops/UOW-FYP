from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    firstname = db.Column(db.String(1000))
    lastname = db.Column(db.String(1000))

class History(UserMixin, db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    task_id = db.Column(db.String(100))
    imagestring = db.Column(db.String(100))
    user_id = db.Column(db.String(100))
    datetime = db.Column(db.String(1000))
    error = db.Column(db.String(1000))