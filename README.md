This is a Login microservice with flask and python

### Login Module


## seminar backend 

pip install flask
pip install sqlalchemy


python
from web import db
from web.models import User, Event, Role, Rolename, Event, Participant
db.create_all()


docker build -t nexr-seminar .
docker run -itd -p 5000:5000 nexr-seminar