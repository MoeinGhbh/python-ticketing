from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.fields.core import IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Role, User
from flask_login import current_user
from wtforms.fields.html5 import DateField


#####################################################      User   ###################################################################

class RegistrationForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(min=3)]
                           )
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(),
                                                     Length(min=3, max=25)])
    confirm_password = PasswordField('confirm password',
                                     validators=[
                                         DataRequired(), EqualTo('password')]
                                     )

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('the user name is already exist.')

    def validate_email(self, email):
        user = User.query.filter_by(username=email.data).first()
        if user:
            raise ValidationError('the email is already exist.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember me')


class UpdateProfile(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('User Name', validators=[DataRequired(), Length(min=3)]
                           )

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('the user name is already exist.')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(username=email.data).first()
            if user:
                raise ValidationError('the email is already exist.')

#####################################################      Event      ###############################################################


class CreateEventForm(FlaskForm):
    event_id = StringField('event ID ', validators=[DataRequired()])
    name = StringField('Event Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    startdate = DateField('Start date', format='%Y-%m-%d')
    enddate = DateField('End date', format='%Y-%m-%d')
    capacity = StringField('Capacity', validators=[DataRequired()])

    # def validate_eventname(self, event_name):
    #     Event.query.filter_by(event_name=event_name)

###################################################         Role        #############################################################


class RolenameForm(FlaskForm):
    # id = StringField('Role Name Id', validators=[DataRequired()])
    role_name = StringField('Role Name', validators=[DataRequired(), Length(min=3)])

#####################################################      Participant     ##########################################################


class AddParticipantForm(FlaskForm):
    name = StringField('participant email', validators=[DataRequired()])
    email = StringField('participant email', validators=[
                        DataRequired(), Email()])


#####################################################      Send Email     ##########################################################

# class sendemailForm(FlaskForm):
#     allevents = SelectField('event name', choices=['Owner', 'Manager'])
