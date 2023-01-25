import os
from unittest import TestCase
from sqlalchemy import exc

from app import app
from models import db, connect_db, User
from forms import LoginForm

connect_db(app)
app.app_context().push()


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

            # test that 4 users were added to the DB
            self.assertEqual(len(users), 4)

    def test_user_login(self):
        '''testing user registration basics'''

        # testing that correct username and password results in successful login
        t_user = 'JerrySeinfeld'
        t_pass = 'whatsthedealwiththat'
        valid_user = User.authenticate_user(t_user, t_pass)

        self.assertEqual(valid_user.username, 'JerrySeinfeld')

    def test_bad_password(self):
        t_other_user = 'GeorgeCostanza'
        self.assertFalse(User.authenticate_user(t_other_user, 'Goretex')) #password has incorrect case (g should be lowercase)

