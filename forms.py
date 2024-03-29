from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateTimeField, BooleanField, SubmitField
from wtforms_alchemy import model_form_factory
from models import db, User, Test, Issue
from wtforms.validators import InputRequired


BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class MessageForm(FlaskForm):
    message = TextAreaField('Message')
    submit = SubmitField('Send message')

    
class RegisterUserForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    email = StringField('Email address') 

# class ChangePasswordForm(FlaskForm):
#     new_password = PasswordField('Password', validators=[InputRequired()])
#     verify_password = PasswordField('Enter Password again', validators=[InputRequired()])

class TestForm(ModelForm):
    class Meta:
        model = Test
        exclude = ['end', 'endday', 'archived']

class IssueForm(ModelForm):
    class Meta:
        model = Issue

class IssueCommentForm(FlaskForm):
    text = TextAreaField('Enter your comment')
    submit = SubmitField('Submit comment!')
