from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from web.models import Role, User
from flask_login import current_user


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


class RoleForm(FlaskForm):
    role_name = StringField('rolename', validators=[
                            DataRequired(), Length(min=3)])


class CreateEvent(FlaskForm):
    event_name = StringField('event name', validators=[DataRequired()])
#     event_id = StringField('event ID ', validators=[DataRequired()])
#     description = StringField('description', validators=[DataRequired()])
#     startdate = StringField('Start date', validators=[DateTimeField()]) # ???????????????
#     enddate = StringField('end date', validators=[DateTimeField()])   # ???????????????
#     capacity = StringField('capacity', validators=[DateTimeField()])
#     ipAddress = StringField('IP Address', validators=[DateTimeField()])

    # def validate_eventname(self, event_name):
    #     Event.query.filter_by(event_name=event_name)


class AddParticipant(FlaskForm):
    name = StringField('participant email', validators=[DataRequired()])
    email = StringField('participant email', validators=[
                        DataRequired(), Email()])
