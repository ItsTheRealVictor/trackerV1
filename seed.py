from models import db, connect_db, User, Test, Issue
from app import app

connect_db(app)
app.app_context().push()

users = [
    {
        'username': 'HankHill',
        'password': 'propane',
        'email': 'hank@strickland.com'
    },
    {
        'username': 'PeggyHill',
        'password': 'boggle',
        'email': 'peggy@boggle.com'
    },
    {
        'username': 'BobbyHill',
        'password': 'comedy',
        'email': 'bobby@thatsmypurse.com'
    },
    {
        'username': 'Boomhauer',
        'password': 'dang',
        'email': 'dangole@talkinbout.com'
    },
]

for user in users:
    new = User.register_user(username=user['username'],
                pwd=user['password'],
                email=user['email'])
    db.session.add(new)
    db.session.commit()

tests = [
    {
        'lot_num': 'RA123456-1',
        'part_num': 'QM54321',
        'test_name': '150C High Temp Storage',
        'location': 'West lab',
        'duration': 500,
        'owner': 'John Redcorn',
    },
    {
        'lot_num': 'RA572487-35',
        'part_num': 'QM54321',
        'test_name': '150C High Temp Storage',
        'location': 'West lab',
        'duration': 500,
        'owner': 'John Redcorn',
    },
    {
        'lot_num': 'RA123456-1',
        'part_num': 'QM54321',
        'test_name': '150C High Temp Storage',
        'location': 'West lab',
        'duration': 500,
        'owner': 'John Redcorn',
    },
    {
        'lot_num': 'RA123456-1',
        'part_num': 'QM54321',
        'test_name': '150C High Temp Storage',
        'location': 'West lab',
        'duration': 500,
        'owner': 'John Redcorn',
    },
    {
        'lot_num': 'RA123456-1',
        'part_num': 'QM54321',
        'test_name': '150C High Temp Storage',
        'location': 'West lab',
        'duration': 500,
        'owner': 'John Redcorn',
    },

]

# for test in tests:
#     new = Test(lot_num=test['lot_num'],
#                part_num=test['part_num'],
#                test_name=test['test_name'],
#                location=test['location'],
#                start=test['start'],
#                location=test['location'],
#                owner=test['owner'])