from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import *
# from app.views.scraping import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class products(db.Model):
    pid = db.Column(db.String(300))
    name = db.Column(db.String(128))
    url = db.Column(db.Text)

class reviews(db.Model):
    pid = db.Column(db.String(300))
    text = db.Column(db.Text)
    title = db.Column(db.String(300))
    polarity = db.Column(db.Float)
    date = db.Column(db.Date)



if __name__ == '__main__':
    manager.run()
    db.create_all()