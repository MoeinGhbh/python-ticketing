from flask import Blueprint, render_template

admin1 = Blueprint("admin", __name__, static_folder='static',template_folder='templates')

@admin1.route('/home')
@admin1.route('/')
def home():
    return render_template('home.html')

@admin1.route('/test')
def test():
    return 'test'