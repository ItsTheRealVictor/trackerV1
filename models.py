from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lot_num = db.Column(db.Text)
    part_num = db.Column(db.Text)
    test_name = db.Column(db.Text)
    location = db.Column(db.Text)
    duration = db.Column(db.Integer)
    owner = db.Column(db.Text)