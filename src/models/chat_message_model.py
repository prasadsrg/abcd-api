from db import db
from models import chat_room_model, profile_model


class ChatMessageModel(db.Model):

    __tablename__ = 'chat_message'

    id = db.Column('id', db.String, primary_key=True)
    profileId = db.Column('profile_id', db.String, db.ForeignKey("profile.id"))
    # profile = db.relationship(profile_model.ProfileModel)
    roomId = db.Column('room_id', db.String, db.ForeignKey("chat_room.id"))
    # room = db.relationship(chat_room_model.ChatRoomModel)
    message = db.Column("message", db.String)
    updatedBy = db.Column('updated_by', db.String)
    updatedOn = db.Column('updated_on', db.DateTime)