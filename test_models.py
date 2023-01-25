import os
from unittest import TestCase
from sqlalchemy import exc

from app import app
from models import db, User


# home computer DB 
# os.environ['DATABASE_URL'] = (os.environ.get('DATABASE_URL', 'postgresql://postgres:admin@localhost/test_user_model'))

# work computer DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trackerV1.db'


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        test_users = [
            {
                'email': 'jerry@superman.com',
                'username': 'JerrySeinfeld',
                'password': 'whatsthedealwiththat',
            },
            {
                'email': 'george@yankees.com',
                'username': 'GeorgeCostanza',
                'password': 'goretex',
            },
            {
                'email': 'elaine@jaypeterman.com',
                'username': 'ElaineBenice',
                'password': 'dance',
            },
            {
                'email': 'kramer@kennyrogerschicken.com',
                'username': 'KosmoKramer',
                'password': 'muffintop',
            },
        ]


        for user in test_users:
            new = User.register_user(username=user['username'],
                        pwd=user['password'],
                        email=user['email'])
            db.session.add(new)
            db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_models(self):
        """Testing User Model basics"""

        users = User.query.all()
        for user in users:

            self.assertEqual(len(user.tests), 0)
            self.assertEqual(len(user.issues), 0)
