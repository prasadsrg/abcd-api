from db import db

class ChatRoomModel(db.Model):

    __tablename__ = 'chat_room'

    id = db.Column('id', db.String, primary_key=True)
    name = db.Column('name', db.String)
    isIndividual = db.Column('is_individual', db.Boolean)
    updatedBy = db.Column('updated_by', db.String)
    updatedOn = db.Column('updated_on', db.DateTime)
    createdBy = db.Column('created_by', db.String)
    createdOn = db.Column('created_on', db.DateTime)