from models import db, connect_db, User, Test, Issue
from app import app
import datetime


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
        'start': datetime.date(2023, 12, 25),
        'owner': 'Kahn Souphanousinphone',
        'end': ''
    },
    {
        'lot_num': 'RA572487-35',
        'part_num': 'QM76222',
        'test_name': '125C Bake',
        'location': 'West lab',
        'start': datetime.date(2023, 10, 4),
        'duration': 24,
        'owner': 'Joseph Gribble',
        'end': ''
    },
    {
        'lot_num': 'RA128346-1',
        'part_num': 'QM79056',
        'test_name': 'UHAST 4',
        'location': 'West lab',
        'start': datetime.date(2022, 6, 14),
        'duration': 96,
        'owner': 'Dale Gribble',
        'end': ''
    },
    {
        'lot_num': 'RA159456-1',
        'part_num': 'QM42069',
        'test_name': '30/60 Soak',
        'location': 'West lab',
        'start': datetime.date(2022, 1, 24),
        'duration': 192,
        'owner': 'Luanne Platter',
        'end': ''
    },
    {
        'lot_num': 'RA127755-1',
        'part_num': 'QM11122',
        'test_name': 'Slow TC',
        'location': 'East lab',
        'start': datetime.date(2023, 1, 1),
        'duration': 332,
        'owner': 'Bill Dautrieve',
        'end': ''
    },

]

for test in tests:
    future_delta = datetime.timedelta(hours=test['duration'])
    future_date = test['start'] + future_delta
    formatted_future_date = future_date.strftime('%a %Y-%m-%d')
    future_date_datetime = datetime.datetime.strptime(formatted_future_date, '%a %Y-%m-%d').date()

    
    new = Test(lot_num=test['lot_num'],
               part_num=test['part_num'],
               test_name=test['test_name'],
               location=test['location'],
               start=test['start'],
               duration=test['duration'],
               owner=test['owner'],
               end=future_date_datetime)

    db.session.add(new)
    db.session.commit()
    
    
issues = [
    {
        'title': 'Propane accessories',
        'text': 'Need to pick up some more propane accessories',
        'username': 'HankHill',
        'date': datetime.date(2022, 5, 5)
    },
    {
        'title': 'Mow lawn',
        'text': 'Need to mow the lawn before the boys come over tomorrow so they dont comment on it.',
        'username': 'HankHill',
        'date': datetime.date(2022, 3, 20)
    },
    {
        'title': 'Boggle practice',
        'text': 'I need to practice for the upcoming boggle championships this weekend',
        'username': 'PeggyHill',
        'date': datetime.date(2022, 6, 14)
    },
    {
        'title': 'Material',
        'text': 'This week I need to work on some material for my upcoming comedy show',
        'username': 'BobbyHill',
        'date': datetime.date(2023, 1, 4)
    },
    {
        'title': 'Study',
        'text': 'Need to meet up with Connie and Joseph this weekend to study',
        'username': 'BobbyHill',
        'date': datetime.date(2021, 11, 11)
    }
]
for issue in issues:
    new = Issue(title=issue['title'], 
                text=issue['text'],
                username=issue['username'],
                date=issue['date'])
    db.session.add(new)
    db.session.commit()
