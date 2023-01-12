from flask import Flask, request, jsonify, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import LoginForm, RegisterUserForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'asdf'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/feedback'
# app.config['SQLALCHEMY_BINDS'] = {'testDB': 'sqlite:///test_feedback.db'}

# use this DB when developing from work computer
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trackerV1.db'

app.debug = False
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPTS_REDIRECTS'] = False

connect_db(app)
app.app_context().push()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        
        register_new_user = User.register_user(username, password, email)
        
        db.session.add(register_new_user)
            
        try:
            db.session.commit()
            
        except IntegrityError:
            form.user.errors.append('Username already exists. Please choose another')
            return render_template('register.html')
        flash('SUCCESS! USER CREATED')
        return redirect('/')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate_user(username, password)
        if user:
            flash(f'Welcome back {user.first_name}')
            session['username'] = user.username
            return redirect('/secret')
        else:
            form.username.errors = ['INVALID PASSORD!']
            
    return render_template('login.html', form=form)
