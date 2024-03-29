from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from iiit_research.models import User,Lab


class CreateLabForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Update image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Create')


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
    user_type = StringField('User Type', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please use a different email.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    password = PasswordField('Password')
    confirm_password = PasswordField('confirm password', validators=[EqualTo('password')])
    about_me = TextAreaField('Write About Your Current Research')
    prof_email = StringField('Professor Email Under whom you are currently working')
    lablist = QuerySelectField('Select Labs',
                               query_factory=lambda: Lab.query.all(),
                               get_label="name"
                               )
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please use a different username.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already in use. Please use a different email.')

    def validate_prof_email(self, prof_email):
        if prof_email.data:
            user = User.query.filter_by(email=prof_email.data).first()
            if not user or user.user_type == 'student':
                raise ValidationError('No Professor is registered with given email. Please use a different email.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    post_as = StringField('Post as')
    file = FileField('Upload File', validators=[FileAllowed(['pdf'])])
    submit = SubmitField('Post')


class SearchForm(FlaskForm):
    query = StringField('Query', validators=[DataRequired()])
    search_for = StringField('Search For', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
