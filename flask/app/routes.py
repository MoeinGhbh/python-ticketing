from flask import Flask, render_template, request, redirect, url_for, flash, abort
from app import app
from app.forms import  CreateEventForm, RegistrationForm, LoginForm, RolenameForm, UpdateProfile, AddParticipantForm
from app.models import User, Role, Rolename, Event, Participant
from app import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/', methods=['GET', 'POST'])
def home():
    event = Event.query.all()
    print(event)
    return render_template('home.html', form=event)


############################################## user login logout register  #####################################################

@app.route('/register', methods=['GET', 'POST'])
def registration():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(
            reg_form.password.data).decode('utf-8')
        new_user = User(username=reg_form.username.data,
                        email=reg_form.email.data, password=hashed_pass)
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

############################################## profile  #####################################################


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

############################################## Event  #####################################################


@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def eventdetail(event_id):
    event = Event.query.get_or_404(event_id)
    # event = Event.query.filter_by(id=event_id)
    return render_template('eventdetail.html', form=event)


@app.route('/event', methods=['GET', 'POST'])
@login_required
def event():
    eventform = CreateEventForm()
    if eventform.validate_on_submit():
        # current_user.rolename = roleform.role_name.data
        print('insert event in data base')
        flash('your event insert successfully', 'info')
        return redirect(url_for('event'))
    elif request.method == 'GET':
        eventform = Event.query.all()
    return render_template('event.html', form=eventform)


@app.route('/event/new', methods=['GET', 'POST'])
@login_required
def new_event():
    form = CreateEventForm()
    if form.validate_on_submit():
        event = Event(name=form.name.data, description=form.description.data, eventowner=current_user,
                      startdate=form.startdate.data, enddate=form.enddate.data, capacity=form.capacity.data)  # eventowner=current_user
        db.session.add(event)
        db.session.commit()
        flash('event created', 'info')
        return redirect(url_for('home'))
    return render_template('create_event.html', form=form)


@app.route('/event/<int:event_id>/delete')
@login_required
def delete(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author != current_user:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('event deleted', 'info')
    return redirect(url_for('home'))


@app.route('/event/<int:event_id>/update', methods=['GET', 'POST'])
@login_required
def update(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author != current_user:
        abort(403)
    form = CreateEventForm()
    if form.validate_on_submit():
        event.name = form.name.data
        event.description = form.description.data
        db.session.commit()
        flash('event updated', 'info')
        return redirect(url_for('detail', event_id=event.id))
    elif request.method == 'GET':
        form.name.data = event.name
        form.description.data = event.description
    return render_template('update.html', form=form)

############################################### Role ######################################################


@app.route('/rolename', methods=['GET', 'POST'])
@login_required
def rolename():
    rolenames = Rolename.query.all()
    print(rolenames)
    return render_template('rolename.html', form=rolenames)


@app.route('/rolenamedetail/<int:rolename_id>', methods=['GET', 'POST'])
@login_required
def rolenamedetail(rolename_id):
    rolenames = Rolename.query.get_or_404(rolename_id)
    return render_template('rolenamedetail.html', form=rolenames)


@app.route('/new_role', methods=['GET','POST'])
@login_required
def new_rolename():
    form = RolenameForm()
    if form.validate_on_submit():
        rolename = Rolename(rolename=form.rolename.data)
        db.session.add(rolename)
        db.session.commit()
        flash('Role created', 'info')
        return redirect(url_for('rolename'))
    return render_template('new_role.html', form=form)


###########################################        participants        ####################################
@app.route('/participant', methods=['GET', 'POST'])
@login_required
def participant():
    participant = Participant.query.all()
    return render_template('participant.html', form=participant)


@app.route('/participant/<int:participant_id>', methods=['GET', 'POST'])
@login_required
def participantDetail(participant_id):
    participantform = AddParticipantForm()
    if participantform.validate_on_submit():
        # current_user.rolename = roleform.role_name.data
        print('insert participant in data base')
        flash('your participant insert successfully', 'info')
        return redirect(url_for('participant'))
    elif request.method == 'GET':
        print('hehehe')
    return render_template('participant.html', form=participantform)


###########################################        Send Email        ####################################

@app.route('/sendemail', methods=['GET', 'POST'])
@login_required
def sendemail():
    return render_template('sendemail.html')
