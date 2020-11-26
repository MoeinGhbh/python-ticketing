from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Weblog.models import User, Post
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(min=3)]
                           )
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(),
                                                     Length(min=3, max=25)])
    confirm_password = PasswordField('confirm password',
                                     validators=[DataRequired(), EqualTo('password')]
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

    # password = PasswordField('password', validators=[DataRequired(),
    #                                                  Length(min=3, max=25)])
    # confirm_password = PasswordField('confirm password',
    #                                  validators=[DataRequired(), EqualTo('password')]
    #                                  )

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


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min=5)])
    content = TextAreaField('content', validators=[DataRequired(), Length(min=10)])
