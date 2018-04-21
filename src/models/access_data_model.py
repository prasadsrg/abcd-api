from db import db

class AccessDataModel(db.Model):
    __tablename__ = 'access_data'

    name = db.Column('name', db.String, primary_key=True)
    code = db.Column('code', db.String)
    val = db.Column('val', db.String)
    data = db.Column('data', db.String)
    status = db.Column('status', db.Boolean)