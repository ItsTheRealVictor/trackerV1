from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime
import time

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
class Message(db.Model):

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default = datetime.datetime.utcnow)

# class IssueComment(db.Model): 

#     __tablename__ = "issue_comments" 

#     id = db.Column(db.Integer, primary_key=True) 
#     author_id = db.Column(db.Integer, db.ForeignKey('users.id')) 
#     issue_comment_author = db.relationship("User", back_populates="issue_comments") 
#     post_id = db.Column(db.Integer, db.ForeignKey('issues.id')) 
#     parent_post = db.relationship("Issue", back_populates="issue_comments")         
#     text = db.Column(db.Text)



class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)

    sent_msgs = db.relationship('Message', foreign_keys=Message.sender_id, backref='author', lazy='dynamic')
    received_msgs = db.relationship('Message', foreign_keys=Message.receiver_id, backref='recipient', lazy='dynamic')

    # issue_comments = db.relationship("IssueComment", back_populates="issue_comment_author")

    def __repr__(self):
        return f'{self.username}'
    
    @classmethod
    def register_user(cls, username, pwd, email):
        
        hashed = bcrypt.generate_password_hash(pwd)
        
        hashed_utf8 = hashed.decode('utf8')
        
        return cls(username=username, 
                   password=hashed_utf8,
                   email=email)
    
    @classmethod
    def authenticate_user(cls, username, pwd):
        
        u = User.query.filter_by(username=username).first()
        
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False
        
class Test(db.Model):

    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lot_num = db.Column(db.Text, info={'label': 'Lot number'})
    part_num = db.Column(db.Text, info={'label': 'Part number'})
    test_name = db.Column(db.Text, info={'label': 'Test name'})
    location = db.Column(db.Text, info={'label': 'Location of test'})
    start = db.Column(db.Date, default=datetime.datetime.utcnow, info={'label': 'Starting date'})
    duration = db.Column(db.Integer, info={'label': 'Test duration (hours)'})
    owner = db.Column(db.Text, info={'label': 'Lot owner'})
    end = db.Column(db.Text)
    endday = db.Column(db.Text)
    archived = db.Column(db.Text, default=False)
        
        

class Issue(db.Model):

    __tablename__ = 'issues'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, info={'label': 'Title'})
    text = db.Column(db.Text, info={'label': 'Issue content'})
    date = db.Column(db.Date, default=datetime.datetime.utcnow, info={'label': 'Date'})
    archived = db.Column(db.Text, default=False)
    comment_text = db.Column(db.Text, info={'label': 'Add a comment'})

    username = db.Column(db.Text, db.ForeignKey('users.username'))
    user = db.relationship('User', backref='Issue')

    # issue_comments = db.relationship('IssueComment', back_populates='parent_post')