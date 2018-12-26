from db import session
from sqlalchemy import func
from utils.util import uid, model_to_dict
from models.chat_user_model import ChatUserModel
from models.chat_room_model import ChatRoomModel
from models.chat_view_model import ChatViewModel
from models.chat_message_model import ChatMessageModel
from mappers.chat_room_mapper import ChatRoomMapper
from mappers.chat_user_mapper import ChatUserMapper
import functools
import datetime


class ChatUserService:

    session_info = None

    def mapping(self, model, view):

        model.room = session.query(ChatRoomModel).filter(id=view["roomId"]).first() if view.get("roomId") \
                                                                                       is not None else ChatRoomModel()
        if model.id is None:
            model.id = uid()
            model.room.id = uid() if view.get("roomId") is None else view.get("roomId")
            model.roomId = model.room.id
            model.room.name = view["name"] if view["isIndividual"] is True else uid()
            model.room.isIndividual = view["isIndividual"]
            model.profileId = view["profileId"]
            model.createdOn = datetime.datetime.now()
            model.createdBy = self.session_info["name"] if self.session_info.get("name") else "SYSTEM"
        model.updatedBy = self.session_info["name"] if self.session_info.get("name") else "SYSTEM"
        model.updatedOn = datetime.datetime.now()
        ChatRoomMapper(model, view.get("room")).model_mapping()
        ChatUserMapper(model, view).model_mapping()

    def is_validate(self, model, is_new):

        query = session.query(ChatUserModel)\
            .filter((ChatUserModel.profileId == model.profileId) | (ChatUserModel.roomId == model.roomId))
        data_list = query.all()
        if data_list:
            if is_new:
                return False
            else:
                for item in data_list:
                    if item.id != model.id:
                        return False
        return True

    def save(self, req_data):
        chat_user = None
        _id = req_data.get('id', None)
        if _id is not None:
            chat_user = session.query(ChatUserModel).filter_by(id=_id).first()
        if chat_user is None:
            chat_user = ChatUserModel()
        self.mapping(chat_user, req_data)
        if self.is_validate(chat_user, False if _id else True):
            session.add(chat_user)
            session.commit()
            return {'message': 'Saved Successfully', 'id': chat_user.id}
        else:
            raise Exception('Record already exists')

    def model(self, _id):
        return session.query(ChatUserModel).filter_by(id=_id).first()

    def search(self, req_data):
        query = session.query(ChatUserModel)
        if req_data and req_data.get('profileId') is not None:
            query = query.filter_by(profileId=req_data["profileId"])
        data_list = query.limit(9999).all()
        data_list = list(map(functools.partial(self.map_room_names, req_data["profileId"]), data_list))
        return data_list

    @staticmethod
    def map_room_names(data, profileId):
        data = model_to_dict(data)
        if data["room"]["isIndividaual"] is True:
            user = session.query(ChatUserModel).filter(
                ChatUserModel.roomId == ChatUserModel.data["roomId"], ChatUserModel.profileId != profileId
            ).first()
            data["room"]["name"] = user.profile.name
        actualMessages = session.query(ChatMessageModel).filter(roomId=data["room"]["id"]).count()
        viewedMessages = session.query(ChatViewModel).filter(
            ChatViewModel.roomId == data["room"]["id"],
            ChatViewModel.profileId == profileId
        ).count()
        data["room"]["unread"] = actualMessages - viewedMessages
        return data