from flask import Flask, request, jsonify, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_change_password import ChangePassword, ChangePasswordForm,  SetPasswordForm
from sqlalchemy import desc, asc
from models import db, connect_db, User, Test, Issue
from forms import LoginForm, RegisterUserForm, TestForm, IssueForm, ChangePasswordForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
import datetime
import calendar

app = Flask(__name__)

flask_change_password = ChangePassword(min_password_length=8, rules=dict(long_password_override=2))
flask_change_password.init_app(app)


app.config['SECRET_KEY'] = 'asdf'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/tracker'
# app.config['SQLALCHEMY_BINDS'] = {'testDB': 'sqlite:///test_tracker.db'}

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




#################### Register/Login/Logout Routes ####################
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
            flash(f'Welcome back {user.username}')
            session['username'] = user.username
            return redirect('/')
        else:
            form.username.errors = ['INVALID PASSWORD!']
            
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username')
    flash('Goodbye')
    return redirect('/')

@app.route('/users/<username>/change_password', methods=['GET', 'POST'])
def change_password(username):
    title = 'Change Password'
    user = User.query.get_or_404(username)
    form = ChangePasswordForm(username=user.username, changing=True, title=title)
    if form.validate_on_submit():
        valid = flask_change_password.verify_password_change_form(form)
        if valid:
            return redirect('/', title='changed', new_password=form.password.data)

        return redirect('/')
    password_template = flask_change_password.change_password_template(form, submit_text='Change')
    return render_template('change_password.html', password_template=password_template, title=title, form=form,
                           user=dict(username=user.username),
                           )




#################### App Function Routes ####################

#################### tests ####################

@app.route('/all_tests')
def dashboard():
    tests = Test.query.order_by(asc(Test.end)).all()
    return render_template('all_tests.html', tests=tests)


@app.route('/users/<username>/tests/add', methods=['GET', 'POST'])
def add_test(username):

    user = User.query.get_or_404(username)
    form = TestForm()


    # I know there's a shorter way to do this but I just can't get it to work. populate_obj(blahblah) or something, 
    # i'm wasting time trying to figure it out so I'm moving on
    if form.validate_on_submit():
        lot_num = form.lot_num.data
        part_num = form.part_num.data
        test_name = form.test_name.data
        location = form.location.data
        start = form.start.data
        duration = form.duration.data
        owner = form.owner.data
        
        
        # calculating future date
        future_delta = datetime.timedelta(hours=duration)
        future_date = start + future_delta
        formatted_future_date = future_date.strftime('%a %Y-%m-%d')
        future_date_datetime = datetime.datetime.strptime(formatted_future_date, '%a %Y-%m-%d').date()        
        future_date_day = future_date_datetime.strftime('%a')      

        
        
        
        new_test = Test(lot_num=lot_num, 
                        part_num=part_num, 
                        test_name=test_name,
                        start=start, 
                        location=location, 
                        duration=duration, 
                        owner=owner,
                        end=future_date_datetime,
                        endday=future_date_day)
    
        db.session.add(new_test)
        db.session.commit()
        return redirect(f'/all_tests')

    return render_template('add_test.html', form=form)


@app.route('/users/tests/<int:test_id>/delete', methods=['GET', 'POST '])
def delete_test(test_id):
    test = Test.query.get_or_404(test_id)
    db.session.delete(test)
    db.session.commit()
    flash('TEST DELETED')
    return redirect('/all_tests')


@app.route('/users/tests/<int:test_id>/edit', methods=['GET', 'POST'])
def edit_test(test_id):
    test = Test.query.get_or_404(test_id)






################################## Issue Routes ###################################
@app.route('/all_issues')
def issues():
    
    issues = Issue.query.order_by(desc(Issue.date)).all()
    
    return render_template('all_issues.html', issues=issues)

@app.route('/users/<username>/issues/add', methods=['GET', 'POST'])
def add_issue(username):

    user = User.query.get_or_404(username)
    form = IssueForm()


    # I know there's a shorter way to do this but I just can't get it to work. populate_obj(blahblah) or something, 
    # i'm wasting time trying to figure it out so I'm moving on
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        username = session['username']

        new_issue = Issue(title=title, text=text, username=username)
    
        db.session.add(new_issue)
        db.session.commit()
        return redirect(f'/all_issues')

    return render_template('add_issue.html', form=form)


@app.route('/users/<username>/issues/<int:issue_id>/delete', methods=['GET', 'POST'])
def delete_issue(username, issue_id):
    issue = Issue.query.get_or_404(issue_id)
    if session['username'] == username:
        db.session.delete(issue)
        db.session.commit()
        return redirect('/all_issues')
