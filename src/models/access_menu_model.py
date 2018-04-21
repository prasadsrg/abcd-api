from db import db


class AccessMenuModel(db.Model):

    __tablename__ = 'access_menu'

    id = db.Column('id', db.String, primary_key=True)
    name = db.Column('name', db.String)
    menu = db.Column('menu', db.String)
    role = db.Column('role', db.String)
    vid = db.Column('vid', db.String)
    active = db.Column('active', db.Boolean)
    priority = db.Column('priority', db.Integer)
    updatedBy = db.Column('updated_by', db.String)
    updatedOn = db.Column('updated_on', db.DateTime)
