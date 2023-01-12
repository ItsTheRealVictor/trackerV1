from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms_alchemy import model_form_factory
from models import db, User, Test
from wtforms.validators import InputRequired


BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    
class RegisterUserForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    email = StringField('Email address') 

class TestForm(ModelForm):
    class Meta:
        model = Test