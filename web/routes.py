from flask import Flask, render_template, request, redirect, url_for, flash, abort
from web import app
from web.forms import AddParticipant, CreateEvent, RegistrationForm, LoginForm, RoleForm, UpdateProfile
from web.models import User
from web import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')





@app.route('/register', methods=['GET', 'POST'])
def registration():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(reg_form.password.data).decode('utf-8')
        new_user = User(username=reg_form.username.data, email=reg_form.email.data, password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        flash('You register successfully.', 'success')
        return redirect(url_for('home'))
    else:
        print('not valid')
    return render_template('registration.html', form=reg_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            # next_page = request.args.get('next')
            flash('You login successfully', 'success')
            return redirect(url_for('home'))
            # return redirect(next_page if next_page else url_for('home'))
        else:
            flash('Email or Password is wrong', 'danger')
    return render_template('login.html', form=login_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('you logged out successfully', 'success')
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    upfrm = UpdateProfile()
    if upfrm.validate_on_submit():
        current_user.email = upfrm.email.data
        current_user.username = upfrm.username.data
        db.session.commit()
        flash('your account update successfully', 'info')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        upfrm.email.data = current_user.email
        upfrm.username.data = current_user.username
    return render_template('profile.html', form=upfrm)


@app.route('/role', methods=['GET', 'POST'])
@login_required
def role():
    roleform = RoleForm()
    if roleform.validate_on_submit():
        # current_user.rolename = roleform.role_name.data
        print('insert role in data base')
        flash('your role insert successfully', 'info')
        return redirect(url_for('role'))
    elif request.method == 'GET':
        print('hehehe')
    return render_template('role.html', form=roleform)


@app.route('/event', methods=['GET', 'POST'])
@login_required
def event():
    eventform = CreateEvent()
    if eventform.validate_on_submit():
        # current_user.rolename = roleform.role_name.data
        print('insert event in data base')
        flash('your event insert successfully', 'info')
        return redirect(url_for('event'))
    elif request.method == 'GET':
        print('hehehe')
    return render_template('event.html', form=eventform)


@app.route('/participant', methods=['GET', 'POST'])
@login_required
def participant():
    participantform = AddParticipant()
    if participantform.validate_on_submit():
        # current_user.rolename = roleform.role_name.data
        print('insert participant in data base')
        flash('your participant insert successfully', 'info')
        return redirect(url_for('participant'))
    elif request.method == 'GET':
        print('hehehe')
    return render_template('participant.html', form=participantform)




