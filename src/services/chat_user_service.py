from db import session
from utils.util import uid
from models.chat_user_model import ChatUserModel
from models.chat_room_model import ChatRoomModel
from mappers.chat_room_mapper import ChatRoomMapper
from mappers.chat_user_mapper import ChatUserMapper
import datetime


class ChatUserService:

    session_info = None

    def mapping(self, model, view):

        if model.id is None:
            model.id = uid()
            model.room = ChatRoomModel()
            model.room.id = uid()
            model.roomId = model.room.id
            model.room.name = view["name"] if view["isIndividual"] is True else uid()
            model.room.isIndividual = view["isIndividual"]
            model.profileId = self.session_info.get("id")
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
        query = query.filter(ChatUserModel.vid == self.session_info['vid'])
        if req_data and req_data.get('name') is not None:
            query = query.filter(ChatUserModel.name.like('%' + req_data['name'] + '%'))
        data_list = query.limit(9999).all()
        return data_list