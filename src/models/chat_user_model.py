from db import db
from models import chat_room_model, profile_model


class ChatUserModel(db.Model):

    __tablename__ = 'chat_user'

    id = db.Column('id', db.String, primary_key=True)
    profileId = db.Column('profile_id', db.String, db.ForeignKey("profile.id"))
    profile = db.relationship(profile_model.ProfileModel)
    roomId = db.Column('room_id', db.String, db.ForeignKey("chat_room.id"))
    room = db.relationship(chat_room_model.ChatRoomModel)
    updatedBy = db.Column('updated_by', db.String)
    updatedOn = db.Column('updated_on', db.DateTime)
    createdBy = db.Column('created_by', db.String)
    createdOn = db.Column('created_on', db.DateTime)