from flask import Flask, request, jsonify, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc, asc
from models import db, connect_db, User, Test, Issue
from forms import LoginForm, RegisterUserForm, TestForm, IssueForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
import datetime
import calendar

app = Flask(__name__)

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
            form.username.errors = ['INVALID PASSORD!']
            
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username')
    flash('Goodbye')
    return redirect('/')

@app.route('/change_password')
def change_password():
    pass


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

@app.route('/users/<username>/tests/archive', methods=['GET', 'POST'])
def view_test_archive(username):
    tests = Test.query.all()
    if session['username'] == username:
        pass

    return render_template('test_archive.html', tests=tests)

@app.route('/users/<username>/<int:test_id>/add_to_archive', methods=['GET', 'POST'])
def archive_test(username, test_id):

    archived_test = Test.query.get_or_404(test_id)
    archived_test.archived = True
    db.session.add(archived_test)
    db.session.commit()
    flash(f'{archived_test.lot_num} has been moved into the archive')

    return redirect('/all_tests')

@app.route('/users/<username>/<int:test_id>/move_out_from_archive', methods=['GET', 'POST'])
def dearchive_test(username, test_id):
    dearchived_test = Test.query.get_or_404(test_id)
    dearchived_test.archived = False
    db.session.add(dearchived_test)
    db.session.commit()
    flash(f'{dearchived_test.lot_num} has been moved out of the archive')
    return redirect(f'/users/{username}/tests/archive')





@app.route('/users/tests/<int:test_id>/edit', methods=['GET', 'POST'])
def edit_test(test_id):
    test = Test.query.get_or_404(test_id)
    pass






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
        return redirect(f'/farts')

    return render_template('add_issue.html', form=form)


@app.route('/users/<username>/issues/<int:issue_id>/delete', methods=['GET', 'POST'])
def delete_issue(username, issue_id):
    issue = Issue.query.get_or_404(issue_id)
    if session['username'] == username:
        db.session.delete(issue)
        db.session.commit()
        return redirect('/farts')

@app.route('/users/<username>/issues/archive', methods=['GET', 'POST'])
def view_issue_archive(username):
    issues = Issue.query.all()

    return render_template('issue_archive.html', issues=issues)

@app.route('/users/<username>/<int:issue_id>/add_to_archive', methods=['GET', 'POST'])
def archive_issue(username, issue_id):

    archived_issue = Issue.query.get_or_404(issue_id)
    archived_issue.archived = True
    db.session.add(archived_issue)
    db.session.commit()
    flash(f'{archived_issue.title} has been moved into the archive')

    return redirect('/farts')

@app.route('/users/<username>/<int:issue_id>/move_out_from_archive', methods=['GET', 'POST'])
def dearchive_issue(username, issue_id):
    dearchived_issue = Issue.query.get_or_404(issue_id)
    dearchived_issue.archived = False
    db.session.add(dearchived_issue)
    db.session.commit()
    flash(f'{dearchived_issue.title} has been moved out of the archive')
    return redirect(f'/users/{username}/issues/archive')
