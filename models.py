from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime
import time

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)
    

class User(db.Model):
    __tablename__ = 'users'
    
    username = db.Column(db.String(20), primary_key=True, unique=True, )
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)

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
        
        

class Issue(db.Model):

    __tablename__ = 'issues'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, info={'label': 'Title'})
    text = db.Column(db.Text, info={'label': 'Issue content'})
    date = db.Column(db.Date, default=datetime.datetime.utcnow, info={'label': 'Date'})

    username = db.Column(db.Text, db.ForeignKey('users.username'))
    user = db.relationship('User', backref='Issue')