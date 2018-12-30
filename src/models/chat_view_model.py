from db import db
from models import chat_room_model, profile_model, chat_message_model


class ChatViewModel(db.Model):

    __tablename__ = 'chat_view'

    id = db.Column('id', db.String, primary_key=True)
    profileId = db.Column('profile_id', db.String, db.ForeignKey("profile.id"))
    profile = db.relationship(profile_model.ProfileModel)
    roomId = db.Column('room_id', db.String, db.ForeignKey("chat_room.id"))
    # room = db.relationship(chat_room_model.ChatRoomModel)
    chatMessageId = db.Column('chat_message_id', db.String, db.ForeignKey("chat_message.id"))
    # chatMessage = db.relationship(chat_message_model.ChatMessageModel)
    isView = db.Column("is_view", db.Boolean)
    updatedBy = db.Column('updated_by', db.String)
    updatedOn = db.Column('updated_on', db.DateTime)
    createdBy = db.Column('created_by', db.String)
    createdOn = db.Column('created_on', db.DateTime)