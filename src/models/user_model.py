from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.String, primary_key=True)
    name = db.Column('name', db.String)
    password = db.Column('password', db.String)
