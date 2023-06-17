from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
from random import choice, randint
from string import ascii_lowercase

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
with app.app_context():
    db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    personalId = db.Column(db.String(50), nullable=False, unique=True)
    phoneNumber = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    businessName = db.Column(db.String(50), nullable=False, default='None')
    balance = db.Column(db.Integer, nullable=False, default=0)
    finances = db.relationship('UserTransactions', backref='person', lazy=True)


class UserTransactions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    transaction = db.Column(db.Integer, nullable=False)
    location = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@app.route('/')
def hello_world():  # put application's code here
    a = db.session.execute(db.select(User)).first()[0]
    jsn = {'name': a.name}
    return jsn


@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        user = User(name=data['firstName'], lastName=data['lastName'], personalId=data['yourId'],
                    phoneNumber=data['phone'], email=data['email'], password=data['password'],
                    businessName=data['businessName'])
        email_check = db.session.execute(db.select(User).filter_by(email=user.email))
        phone_number_check = db.session.execute(db.select(User).filter_by(phoneNumber=user.phoneNumber))
        id_check = db.session.execute(db.select(User).filter_by(personalId=user.personalId))
        if bool(email_check):
            return {'responseMessage': "Email Already Exists."}
        if bool(phone_number_check):
            return {'responseMessage': 'Phone Number Already Exists.'}
        if bool(id_check):
            return {'responseMessage': 'Personal ID Already Exists.'}
        db.session.add(user)
        db.session.commit()
        return 'muwuka'
    else:
        return 'muwuka'


@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        check = db.session.execute(db.select(User).filter_by(email=data['email'], password=data['password'])).first()

        print(bool(check))
        response = {'resp': bool(check)}
        return response
    else:
        return 'muwuka'


# with app.app_context():
#     with open(r'C:\Users\ttsul\Desktop\სახელები.txt', encoding='UTF-8') as f:
#         qalaqebi = [line.strip().split('\t')[1] for line in f.readlines()]
#     for _ in range(5):
#         for user in db.session.execute(db.select(User)).scalars():
#             transaction = randint(1, 100) * 5
#             location = choice(qalaqebi)
#             date = datetime(2023, randint(1, 12), randint(1, 28))
#             transact = UserTransactions(date=date, location=location, transaction=transaction, userId=user.id)
#             db.session.add(transact)
#         db.session.commit()
