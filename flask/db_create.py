from app import db
from app.models import User, Event, Role, Rolename, Participanttypes
from app import db, bcrypt


import secrets

secrets.token_hex(16)


db.create_all()

hashed_pass = bcrypt.generate_password_hash("123").decode("utf-8")
new_user = User(username="admin", email="admin@vriday.net", password=hashed_pass)
db.session.add(new_user)
db.session.commit()

new_rolename = Rolename(role_name="admin")
db.session.add(new_rolename)
db.session.commit()

new_role = Role(rolename_id=1, user_id=1)
db.session.add(new_role)
db.session.commit()

new_rolename = Rolename(role_name="event_owner")
db.session.add(new_rolename)
db.session.commit()


new_participanttyps = Participanttypes(type="Participant")
db.session.add(new_participanttyps)
db.session.commit()

new_participanttyps_2 = Participanttypes(type="Presenter")
db.session.add(new_participanttyps_2)
db.session.commit()


print("DB created.")
