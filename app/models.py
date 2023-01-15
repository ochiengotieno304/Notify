from . import db
from flask_login import UserMixin
import datetime
from sqlalchemy import Column, Integer, DateTime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    reg = db.Column(db.String(30))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(20))
    school = db.Column(db.String(50))

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.Text)
    # created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


