class Products(db.Model):
    pid = db.Column(db.String(300), primary_key=True)
    name = db.Column(db.String(128))
    url = db.Column(db.Text)

class Reviews(db.Model):
    pid = db.Column(db.String(300), primary_key=True)
    text = db.Column(db.Text)
    title = db.Column(db.String(300))
    polarity = db.Column(db.Float)
    date = db.Column(db.Date)

