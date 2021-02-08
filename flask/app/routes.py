from flask import Flask, render_template, request, redirect, url_for, flash, abort
from app import app
from app.forms import CreateEventForm, RegistrationForm, LoginForm, RolenameForm, UpdateProfile, AddParticipantForm, RoleForm
from app.models import User, Role, Rolename, Event, Participant
from app import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import re


@app.route('/', methods=['GET', 'POST'])
def home():
    event = Event.query.limit(5).all()
    return render_template('home.html', form=event)


############################################## user login logout   #####################################################


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

############################################## user    #####################################################


@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    users = User.query.all()
    return render_template('Users.html', form=users)


@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def userdetail(user_id):
    users = User.query.get_or_404(user_id)
    return render_template('userdetail.html', form=users)


@app.route('/userdetail/<int:user_id>/update', methods=['GET', 'POST'])
@login_required
def user_update(user_id):
    users = User.query.get_or_404(user_id)
    if current_user.username != 'admin':
        abort(403)
    form = UpdateProfile()
    if request.method == 'POST':
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.match(regex, form.email.data):
            users.username = form.username.data
            users.email = form.email.data
            db.session.commit()
            flash('user updated', 'info')
            return redirect(url_for('userdetail', user_id=users.id))
        else:
            flash('email address is not valid')
            return redirect(url_for('user_update', user_id=users.id))
    elif request.method == 'GET':
        form.username.data = users.username
        form.email.data = users.email
        form.id = users.id
    return render_template('user_update.html', form=form)


@app.route('/userdetail/<int:user_id>/delete')
@login_required
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.username != 'admin':
        abort(403)
    db.session.delete(user)
    try:
        db.session.commit()
        flash('user deleted', 'info')
        return redirect(url_for('users'))
    except:
        flash('Can not delete this user', 'danger')
        return redirect(url_for('userdetail', user_id=user_id))


@app.route('/register', methods=['GET', 'POST'])
def registration():
    if current_user.username != 'admin':
        abort(403)
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(
            reg_form.password.data).decode('utf-8')
        new_user = User(username=reg_form.username.data,
                        email=reg_form.email.data, password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        flash('You register successfully.', 'success')
        return redirect(url_for('users'))
    else:
        print('not valid')
    return render_template('registration.html', form=reg_form)

############################################## user Role  #####################################################


@app.route('/userdetail/<int:user_id>/role')
@login_required
def user_role(user_id):
    print(current_user)
    if current_user.username != 'admin':
        abort(403)
    roleform = RoleForm()
    user = User.query.get_or_404(user_id)
    roleform.username = user.username
    roleform.user_id = user.id

    roleform.role.choices = [(rolename.id, rolename.role_name)
                             for rolename in Rolename.query.all()]
    roleform.role.default = '1'  # set admin as defailt value
    roleform.process()

    users_roles = Role.query.filter_by(user_id=user_id)
    myRole = ''
    for x in users_roles:
        myRole += x.rolename.role_name + '  ,'

    roleform.roles = myRole
    return render_template('user_role.html', form=roleform)


@app.route('/userdetail/<int:user_id>/<int:role_id>/insert')
@login_required
def roles_insert(user_id, role_id):
    roleform = RoleForm()
    print(request.method)
    if request.method == 'POST' or request.method == 'GET':
        print(user_id, role_id)
        checkRole = Role.query.filter_by(
            rolename_id=role_id, user_id=user_id).first()
        print(checkRole)
        if checkRole:
            flash('This role is already assigned to the user', 'danger')
            return redirect(url_for('user_role', user_id=user_id))
        else:
            new_user_role = Role(rolename_id=role_id, user_id=user_id)
            db.session.add(new_user_role)
            db.session.commit()
            flash('A new role is assigned to the user', 'success')
            return redirect(url_for('user_role', user_id=user_id))


@app.route('/userdetail/<int:user_id>/<int:role_id>/delete')
@login_required
def roles_delete(user_id, role_id):
    print(user_id, role_id)
    role = Role.query.filter_by(user_id=user_id, rolename_id=role_id).first()
    if role:
        db.session.delete(role)
        db.session.commit()
        flash('role deleted', 'info')
        return redirect(url_for('user_role', user_id=user_id))
    else:
        flash('this role does not exist', 'danger')
        return redirect(url_for('user_role', user_id=user_id))


############################################## Event  #####################################################


@app.route('/event', methods=['GET', 'POST'])
@login_required
def event():
    eventform = Event.query.limit(5).all()
    return render_template('event.html', form=eventform)


page_siz = 5
page = 0


@app.route('/event/<float(signed=True):move>/paging', methods=['GET', 'POST'])
@login_required
def paging(move):
    global page_siz
    global page
    all = Event.query.all()
    MaxPage = (len(all)//5)
    if (len(all) % 5) > 0:
        MaxPage += 1
    if move == 1:
        if page < MaxPage:
            page += 1
    else:
        if page > 1:
            page -= 1
    end = page * page_siz
    first = (page * page_siz)-5
    eventform = Event.query.limit(end).all()
    eventform = eventform[first:]
    return render_template('event.html', form=eventform)


homepage_siz = 5
homepage = 0


@app.route('/<float(signed=True):move>/homepaging', methods=['GET', 'POST'])
@login_required
def homePaging(move):
    global homepage_siz
    global homepage
    all = Event.query.all()
    MaxPage = (len(all)//5)
    if (len(all) % 5) > 0:
        MaxPage += 1
    if move == 1:
        if homepage < MaxPage:
            homepage += 1
    else:
        if homepage > 1:
            homepage -= 1
    end = homepage * homepage_siz
    first = (homepage * homepage_siz)-5
    eventform = Event.query.limit(end).all()
    eventform = eventform[first:]
    print(first)
    print(end)
    return render_template('home.html', form=eventform)


@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def eventdetail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('eventdetail.html', form=event)


@app.route('/event/new', methods=['GET', 'POST'])
@login_required
def new_event():
    form = CreateEventForm()
    regex = '\d+'
    if re.match(regex, str(form.capacity.data)):
        if request.method == "POST":
            event = Event(name=form.name.data, description=form.description.data, eventowner=current_user,
                          startdate=form.startdate.data, enddate=form.enddate.data, capacity=form.capacity.data)  # eventowner=current_user
            db.session.add(event)
            db.session.commit()
            flash('event created', 'info')
            return redirect(url_for('event'))
    else:
        flash('please enter number', 'danger')
        return render_template('create_event.html', form=form)


@app.route('/event/<int:event_id>/delete')
@login_required
def delete(event_id):
    event = Event.query.get_or_404(event_id)
    # if event.author != current_user:
    #     abort(403)
    try:
        db.session.delete(event)
        db.session.commit()
        flash('event deleted', 'info')
        return redirect(url_for('event'))
    except:
        flash('this event has participants', 'danger')
        return redirect(url_for('eventdetail', event_id=event_id))


@app.route('/event/<int:event_id>/update', methods=['GET', 'POST'])
@login_required
def update(event_id):
    event = Event.query.get_or_404(event_id)
    print(event.user_id)
    # print(current_user.username)
    # if current_user.username == 'admin':
    #     abort(403)
    form = CreateEventForm()
    print('form.users.data', form.users.data)

    if request.method == 'POST':
        event.name = form.name.data
        event.description = form.description.data
        event.startdate = form.startdate.data
        event.enddate = form.enddate.data
        event.capacity = form.capacity.data
        event.user_id = form.users.data
        db.session.commit()
        flash('event updated', 'info')
        return redirect(url_for('eventdetail', event_id=event.id))
    elif request.method == 'GET':
        # make user dropdown
        user = User.query.all()
        form.users.choices = [(users.id, users.username)
                              for users in User.query.all()]
        form.users.default = event.user_id
        form.process()
        ########
        form.name.data = event.name
        form.description.data = event.description
        form.event_id.data = event.id
        form.startdate.data = event.startdate
        form.enddate.data = event.enddate
        form.capacity.data = event.capacity
        return render_template('update.html', form=form)

############################################### Role Name ######################################################


@app.route('/rolename', methods=['GET', 'POST'])
@login_required
def rolename():
    rolenames = Rolename.query.all()
    return render_template('rolename.html', form=rolenames)


@app.route('/rolenamedetail/<int:rolename_id>', methods=['GET', 'POST'])
@login_required
def rolenamedetail(rolename_id):
    rolenames = Rolename.query.get_or_404(rolename_id)
    return render_template('rolenamedetail.html', form=rolenames)


@app.route('/new_role', methods=['GET', 'POST'])
@login_required
def new_rolename():
    form = RolenameForm()
    if form.validate_on_submit():
        rolename = Rolename.query.filter_by(
            role_name=form.role_name.data).first()
        if rolename:
            flash('thid Role already exist', 'danger')
            return render_template('new_role.html', form=form)
        else:
            rolename = Rolename(role_name=form.role_name.data)
            db.session.add(rolename)
            db.session.commit()
            flash('Role created', 'info')
            return redirect(url_for('rolename'))
    return render_template('new_role.html', form=form)


@app.route('/rolenamedetail/<int:role_id>/delete')
@login_required
def role_delete(role_id):
    role = Rolename.query.get_or_404(role_id)
    user_role = Role.query.filter_by(rolename_id=role_id).first()
    print(user_role)
    if user_role:
        flash('this Role assigned to user', 'danger')
        return render_template('rolenamedetail.html', form=role)
    else:
        db.session.delete(role)
        db.session.commit()
        flash('The Role deleted', 'info')
        return redirect(url_for('rolename'))


@app.route('/rolenamedetail/<int:role_id>/update', methods=['GET', 'POST'])
@login_required
def role_update(role_id):
    rolename = Rolename.query.get_or_404(role_id)
    form = RolenameForm()
    if form.validate_on_submit():
        rolename.role_name = form.role_name.data
        db.session.commit()
        flash('role updated', 'info')
        return redirect(url_for('rolenamedetail', rolename_id=rolename.id))
    elif request.method == 'GET':
        form.role_name.data = rolename.role_name
        form.id.data = rolename.id
    return render_template('rolename_update.html', form=form)

###########################################        participants        ####################################


@app.route('/participant/<int:event_id>', methods=['GET', 'POST'])
@login_required
def participant(event_id):
    participant = Participant.query.filter_by(event_id=event_id)
    event_name = ''
    if Event.query.filter_by(id=event_id).first():
        event_name = Event.query.filter_by(id=event_id).first().name
    return render_template('participant.html', form=participant, event_id=event_id, event_name=event_name)


@app.route('/new_participant/<int:event_id>/<string:event_name>', methods=['POST', 'GET'])
@login_required
def new_participant(event_id, event_name):
    print(event_id, event_name)
    form = AddParticipantForm()
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if request.method == "POST":
        print('new participants')
        if re.match(regex, str(form.email.data)):
            check_participant = Participant.query.filter_by(
                email=form.email.data, event_id=event_id).first()
            if check_participant:
                flash('this participant already exist', 'danger')
                return redirect(url_for('new_participant', event_id=event_id, event_name=event_name))
            else:
                new_participant = Participant(
                    name=form.name.data, email=form.email.data, event_id=event_id)
                db.session.add(new_participant)
                db.session.commit()
                flash('Participante successfully added', 'info')
                return redirect(url_for('participant', event_id=event_id))
        else:
            flash('please enter valid email address', 'danger')
            return redirect(url_for('new_participant', event_id=event_id, event_name=event_name))
    else:
        form.event_name.data = event_name
        form.event_id.data = event_id
    return render_template('new_participant.html', form=form)


@app.route('/participantDetail/<int:participant_id>/<int:event_id>', methods=['GET', 'POST'])
@login_required
def participantDetail(participant_id, event_id):
    form = AddParticipantForm()
    print(request.method)
    if request.method == 'POST':
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.match(regex, str(form.email.data)):
            participant = Participant.query.get_or_404(participant_id)
            participant.name = form.name.data
            participant.email = form.email.data
            db.session.commit()
            flash('Participant updated', 'info')
            return redirect(url_for('participantDetail', participant_id=participant_id, event_id=participant.event_id))
        else:
            flash('Please enter valid address', 'danger')
            return redirect(url_for('participantDetail', participant_id=participant_id, event_id=event_id))
    else:
        participantform = AddParticipantForm()
        participant = Participant.query.filter_by(
            id=participant_id, event_id=event_id).first()
        participantform.name.data = participant.name
        participantform.email.data = participant.email
        participantform.event_id.data = event_id
        participantform.id.data = participant_id
        return render_template('participant_update.html', form=participantform)


@app.route('/participantDetail/<int:participant_id>/delete', methods=['GET', 'POST'])
@login_required
def participant_delete(participant_id):
    participant = Participant.query.get_or_404(participant_id)
    db.session.delete(participant)
    db.session.commit()
    flash('Participant delete', 'info')
    return redirect(url_for('participantDetail', participant_id=participant_id, event_id=participant.event_id))

###########################################        Send Email        ####################################


@app.route('/sendemail', methods=['GET', 'POST'])
@login_required
def sendemail():
    return render_template('sendemail.html')
