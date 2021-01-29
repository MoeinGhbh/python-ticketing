from app import db
from app.models import User, Event, Role, Rolename, Participant

db.create_all()

print("DB created.")