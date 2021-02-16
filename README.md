###  Seminar Backend playground


To develop locally, create a new virtual env in the `flask` directory & run the app:

## Command prompt
cd app
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python run.py
## after run
Go to - http://127.0.0.1:5000


To run the container locally:

## Command line
docker-compose up --build
## after run
Go to - http://127.0.0.1/



### Notes

`nginx` logs and `uwsgi` logs will be logged to `log/nginx` and `log/uwsgi` respectively. This can be changed by changing the `volume` mounts in the `docker-compose.yml`.
Alternatively, delete the `volumes` to have Docker log to `Stdout`.

pipenv lock -r > requirements.txt





