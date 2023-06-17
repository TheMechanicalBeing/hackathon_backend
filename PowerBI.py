from openpyxl import Workbook, load_workbook
from csv import DictWriter
from app import app, db, User, UserTransactions

with open("data.csv", 'w', encoding='UTF-8') as f:
    writer = DictWriter(f, fieldnames=['name', 'location', 'time', 'transaction'])
    writer.writerow({'name': 'Name', 'location': 'Location', 'time': 'Time', 'transaction': 'Transaction'})
    with app.app_context():
        for transaction in db.session.execute(db.select(db.select(UserTransactions)))
