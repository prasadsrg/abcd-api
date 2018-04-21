from db import db

class AddressModel(db.Model):
    __tablename__ = 'address'

    id = db.Column('id', db.String, primary_key=True)
    lane = db.Column('lane', db.String)
    landMark = db.Column('land_mark', db.String)
    city = db.Column('city', db.String)
    state = db.Column('state', db.String)
    country = db.Column('country', db.String)
    zipcode = db.Column('zipcode', db.Integer)