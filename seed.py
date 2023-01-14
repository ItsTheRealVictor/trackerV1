from models import db, connect_db, User, Test, Issue
from app import app

connect_db(app)
app.app_context().push()

db.drop_all()
db.create_all()



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
        'part_num': 'QM54534',
        'test_name': '150C High Temp Storage',
        'location': 'West lab',
        'duration': 500,
        'start': '2023-12-25',
        'owner': 'Kahn Souphanousinphone',
    },
    {
        'lot_num': 'RA572487-35',
        'part_num': 'QM76222',
        'test_name': '125C Bake',
        'location': 'West lab',
        'start': '2023-10-04',
        'duration': 24,
        'owner': 'Joseph Gribble',
    },
    {
        'lot_num': 'RA128346-1',
        'part_num': 'QM79056',
        'test_name': 'UHAST 4',
        'location': 'West lab',
        'start': '2022-06-14',
        'duration': 96,
        'owner': 'Dale Gribble',
    },
    {
        'lot_num': 'RA159456-1',
        'part_num': 'QM42069',
        'test_name': '30/60 Soak',
        'location': 'West lab',
        'start': '2022-01-24',
        'duration': 192,
        'owner': 'Luanne Platter',
    },
    {
        'lot_num': 'RA127755-1',
        'part_num': 'QM11122',
        'test_name': 'Slow TC',
        'location': 'East lab',
        'start': '2023-01-01',
        'duration': 332,
        'owner': 'Bill Dautrieve',
    },

]

for test in tests:
    new = Test(lot_num=test['lot_num'],
               part_num=test['part_num'],
               test_name=test['test_name'],
               location=test['location'],
               start=test['start'],
               duration=test['duration'],
               owner=test['owner'])

    db.session.add(new)
    db.session.commit()