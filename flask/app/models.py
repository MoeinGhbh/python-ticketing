from app import db, login_manager
import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Rolename(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String, nullable=False, unique=True)
    roles = db.relationship('Role', backref='rolename', lazy=True)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id},{self.role_name})'



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    events = db.relationship('Event', backref='eventowner', lazy=True)
    roles = db.relationship('Role', backref='roleuser', lazy=True)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.username})'


class Role(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    rolename_id = db.Column(db.Integer, db.ForeignKey('rolename.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id})'


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    startdate = db.Column(db.DateTime, nullable=False,
                          default=datetime.datetime.now)
    enddate = db.Column(db.Text, nullable=False)
    capacity = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.name},{self.description[:30]}, {self.startdate}, {self.enddate},{self.capacity})'


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=True)
    email = db.Column(db.String(50), nullable=False)
    event_id = db.Column(db.ForeignKey('event.id'), nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.name},{self.email})'
