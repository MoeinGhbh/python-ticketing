from flask import Blueprint, render_template

profile1 = Blueprint("profile", __name__, static_folder='static',template_folder='templates')

@profile1.route('/profile')
@profile1.route('/')
def profile():
    return render_template('profile.html')

@profile1.route('/testprofile')
def test():
    return 'test_profile'