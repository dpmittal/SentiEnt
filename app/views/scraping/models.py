from app import *
from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)

engine = create_engine('postgresql://'+app.config['DBUSER']+':'+app.config['PASSWORD']+'@'+app.config['HOST']+':5432/'+app.config['DBNAME'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

class Products(db.Model):
    pid = db.Column(db.String(300), primary_key=True)
    name = db.Column(db.String(300))
    url = db.Column(db.Text)

    def __repr__(self):
        return '<Product %r>' % self.pid

class Reviews(db.Model):
    __tablename__ = 'reviews'
    id= db.Column(db.Integer,primary_key=True, autoincrement = True)
    pid = db.Column(db.String(300),db.ForeignKey('products.pid'))
    text = db.Column(db.Text)
    title = db.Column(db.String(300))
    polarity = db.Column(db.Float)
    date = db.Column(db.Date)

    def __repr__(self):
        return '<Reviews %r>' % self.title
