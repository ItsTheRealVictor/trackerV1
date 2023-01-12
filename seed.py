from models import db, User, connect_db
from app import app

connect_db(app)
app.app_context().push()

example = User(username='example', password='password', email='email.com')

reg_example = User.register_user(username=example.username, pwd=example.password)



db.session.add(reg_example)
db.session.commit()