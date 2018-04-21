from db import db

class AppDataModel(db.Model):

    __tablename__ = 'app_data'

    id = db.Column('id', db.String, primary_key=True)
    name = db.Column('name', db.String)
    code = db.Column('code', db.String)
    data = db.Column('data', db.String)
    active = db.Column('active', db.Boolean)
    vid = db.Column('vid', db.String)
    updatedBy = db.Column('updated_by', db.String)
    updatedOn = db.Column('updated_on', db.DateTime)