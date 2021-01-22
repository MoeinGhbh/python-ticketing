from enum import unique
from web import db, login_manager
import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.username}/' \
               f'{self.email})'


class Role(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(20), nullable=False)


class Event(db.Model, UserMixin):
    event_id = db.Column(db.Integer, primary_key=True)
    eventid = db.Column(db.String, nullable=False)
    eventname = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(150))
    startdate = db.Column(db.DateTime, nullable=False)
    enddate = db.Column(db.DateTime, nullable=False)
    capacity = db.Column(db.Integer)
    ipAddress = db.Column(db.String)


class participant(db.Model, UserMixin):
    participant_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(50))
    event_id = db.Column(db.String(50))  # ???????
