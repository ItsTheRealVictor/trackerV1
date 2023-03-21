from flask import Flask, request, jsonify, render_template, redirect, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc, asc
from models import db, connect_db, User, Test, Issue, Message
from forms import LoginForm, RegisterUserForm, TestForm, IssueForm, MessageForm, IssueCommentForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
import datetime
import calendar



CURR_USER_KEY = 'curr_user'
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


@app.before_request
def add_user_to_g():
    
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    session[CURR_USER_KEY] = user.id
    pass
    

def do_logout():
    
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    flash('LOGGED OUT')
    return redirect('/login')


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
            do_login(register_new_user)
            
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
            do_login(user)
            flash(f'Welcome back {user.username}')
            return redirect('/')
        else:
            form.username.errors = ['INVALID PASSORD!']
            
    return render_template('login.html', form=form)
            

@app.route('/logout')
def logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    
    flash('Goodbye')
    return redirect('/')

#################### App Function Routes ####################

############################## User routes #################################

@app.route('/users/all', methods=['GET', 'POST'])
def get_all_users():
    users = User.query.all()
    return render_template('all_users.html', users=users)

@app.route('/users/<int:user_id>/info', methods=['GET', 'POST'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('single_user.html', user=user)













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


@app.route('/users/<username>/tests/<int:test_id>/delete', methods=['GET', 'POST '])
def delete_test(username, test_id):
    test = Test.query.get_or_404(test_id)
    db.session.delete(test)
    db.session.commit()
    flash('TEST DELETED')
    return redirect('/all_tests', username=username)

@app.route('/users/<username>/tests/archive', methods=['GET', 'POST'])
def view_test_archive(username):
    tests = Test.query.all()
    if session['username'] == username:
        pass

    return render_template('test_archive.html', tests=tests)

@app.route('/users/<username>/tests/<int:test_id>/add_to_archive', methods=['GET', 'POST'])
def archive_test(username, test_id):

    archived_test = Test.query.get_or_404(test_id)
    archived_test.archived = True
    db.session.add(archived_test)
    db.session.commit()
    flash(f'{archived_test.lot_num} has been moved into the archive')

    return redirect('/all_tests')

@app.route('/users/<username>/tests/<int:test_id>/move_out_from_archive', methods=['GET', 'POST'])
def dearchive_test(username, test_id):
    dearchived_test = Test.query.get_or_404(test_id)
    dearchived_test.archived = False
    db.session.add(dearchived_test)
    db.session.commit()
    flash(f'{dearchived_test.lot_num} has been moved out of the archive')
    return redirect(f'/users/{username}/tests/archive')





@app.route('/users/<username>/tests/<int:test_id>/edit', methods=['GET', 'POST'])
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
        return redirect(f'/all_issues')

    return render_template('add_issue.html', form=form)

@app.route('/users/<username>/issues/<int:issue_id>/add_comment', methods=['GET', 'POST'])
def add_issue_comment(username, issue_id):
    username = g.user.username
    issue= Issue.query.filter_by(id = issue_id).all()
    form = IssueCommentForm()
    if form.validate_on_submit():
        issue[0].title = issue[0].title
        issue[0].text = issue[0].text
        issue[0].date = issue[0].date
        issue[0].archived = issue[0].archived
        issue[0].comment_text = form.text.data if form.text.data else 'no comment'

        db.session.add(issue[0])
        db.session.commit()
        flash('COMMENT ADDED')
        return redirect('/all_issues')

    return render_template('add_comment.html', username=username, form=form, issue=issue)









@app.route('/users/<username>/issues/<int:issue_id>/delete', methods=['GET', 'POST'])
def delete_issue(username, issue_id):
    issue = Issue.query.get_or_404(issue_id)
    if session['username'] == username:
        db.session.delete(issue)
        db.session.commit()
        return redirect('/all_issues')

@app.route('/users/<username>/issues/archive', methods=['GET', 'POST'])
def view_issue_archive(username):
    issues = Issue.query.all()

    return render_template('issue_archive.html', issues=issues)

@app.route('/users/<username>/issues/<int:issue_id>/add_to_archive', methods=['GET', 'POST'])
def archive_issue(username, issue_id):

    archived_issue = Issue.query.get_or_404(issue_id)
    archived_issue.archived = True
    db.session.add(archived_issue)
    db.session.commit()
    flash(f'{archived_issue.title} has been moved into the archive')

    return redirect('/all_issues')

@app.route('/users/<username>/issues/<int:issue_id>/move_out_from_archive', methods=['GET', 'POST'])
def dearchive_issue(username, issue_id):
    dearchived_issue = Issue.query.get_or_404(issue_id)
    dearchived_issue.archived = False
    db.session.add(dearchived_issue)
    db.session.commit()
    flash(f'{dearchived_issue.title} has been moved out of the archive')
    return redirect(f'/users/{username}/issues/archive')


#################################### Message Routes ########################################################

@app.route('/users/<int:user_id>/messages', methods=['GET', 'POST'])
def get_messages(user_id):
    user_id = g.user.id
    messages = g.user.received_msgs.all()

    return render_template('messages.html', messages=messages)

@app.route('/users/<int:recipient_id>/send_message', methods=['GET', 'POST'])
def send_message(recipient_id):
    recipient = User.query.filter_by(id=recipient_id).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=g.user, recipient=recipient, body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('MESSAGE SENT!')
        return redirect(f'/')
    return render_template('send_message.html', form=form, recipient=recipient)

@app.route('/users/<int:message_id>/delete_message', methods=['GET', 'POST'])
def delete_message(message_id):
    
    user_id = g.user.id
    msg = Message.query.get(message_id)
    db.session.delete(msg)
    db.session.commit()
    
    return redirect(f'/users/{user_id}/messages')
