from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.core import IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, \
    EqualTo, ValidationError
from app.models import User, Event
from wtforms.fields.html5 import DateField

####################      User   ##################


class RegistrationForm(FlaskForm):
    username = StringField("User Name", validators=[
                           DataRequired(), Length(min=3)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "password", validators=[DataRequired(), Length(min=8, max=25)]
    )
    confirm_password = PasswordField(
        "confirm password", validators=[DataRequired(), EqualTo("password")]
    )

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("the user name is already exist.")

    def validate_email(self, email):
        user = User.query.filter_by(username=email.data).first()
        if user:
            raise ValidationError("the email is already exist.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    remember = BooleanField("Remember me")


class UpdateProfile(FlaskForm):
    id = StringField("id")
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("User Name", validators=[
                           DataRequired(), Length(min=3)])

    def validate_username(self, username):
        # if current_user.username != username.data:
        user = User.query.filter_by(username=username.data).first()
        print(user)
        if user:
            raise ValidationError("the user name is already exist.")

    def validate_email(self, email):
        # if current_user.email != email.data:
        user = User.query.filter_by(username=email.data).first()
        if user:
            raise ValidationError("the email is already exist.")

#############      Event      #################


class CreateEventForm(FlaskForm):
    event_id = StringField("event ID ", validators=[DataRequired()])
    name = StringField("Event Name", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    startdate = DateField("Start date", format="%Y-%m-%d")
    enddate = DateField("End date", format="%Y-%m-%d")
    capacity = IntegerField("Capacity", validators=[DataRequired()])
    event_owner = StringField("Event Owner")
    users = SelectField("Users")

    def validate_event(self, event):
        print("sdgolsiadjfsejdfliauhsdfiouhaedsuifhasduyfasdyu")
        event = Event.query.filter_by(name=event).first()
        if event:
            raise ValidationError("the event name is already exist.")

###################         Role Name       ####################


class RolenameForm(FlaskForm):
    id = StringField("id")
    role_name = StringField("Role Name", validators=[
                            DataRequired(), Length(min=3)])

###################         Role        ########################


class RoleForm(FlaskForm):
    role = SelectField("Role")
    username = StringField("User name")
    user_id = StringField("User id")
    roles = StringField("User" "s role")


####################      Participant     #######################


class AddParticipantForm(FlaskForm):
    id = StringField("id")
    name = StringField("Participant Name", validators=[DataRequired()])
    email = StringField("Participant E-mail",
                        validators=[DataRequired(), Email()])
    events = SelectField("event")
    event_name = StringField("Event Name")
    event_id = StringField("Event ID")
    participant_type = SelectField("Participant Type")
