from db import db

class VendorModel(db.Model):

    __tablename__ = 'vendor'

    id = db.Column('id', db.String, primary_key=True)
    name = db.Column('name', db.String)
    title = db.Column('title', db.String)
    logo = db.Column('logo', db.Text)
    status = db.Column('status', db.Boolean)
