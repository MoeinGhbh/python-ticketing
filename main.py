from flask import Flask
from admin.admin import admin1
from clients.profile import profile1

app=Flask(__name__)
app.register_blueprint(admin1,  url_prefix='/admin')
app.register_blueprint(profile1, url_prefix='/profile')

@app.route('/')
def main():
    return '<h3>rose raeein</h3>'

if __name__=='__main__':
    app.run(debug=True)