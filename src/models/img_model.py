from db import db

class ImgModel(db.Model):
    __tablename__ = 'img'

    id = db.Column('id', db.String, primary_key=True)
    name = db.Column('name', db.String)
    src = db.Column('src', db.String)
