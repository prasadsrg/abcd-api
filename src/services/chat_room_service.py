from db import session
from utils.util import uid
from models.chat_room_model import ChatRoomModel
from mappers.chat_room_mapper import ChatRoomMapper
import datetime


class ChatRoomService:

    session_info = None

    def mapping(self, model, view):

        if model.id is None:
            model.id = uid()
            model.name = view["name"] if view["isIndividual"] is True else uid()
            model.isIndividual = view["isIndividual"]
            model.createdOn = datetime.datetime.now()
            model.createdBy = self.session_info["name"] if self.session_info.get("name") else "SYSTEM"
        model.updatedBy = self.session_info["name"] if self.session_info.get("name") else "SYSTEM"
        model.updatedOn = datetime.datetime.now()
        ChatRoomMapper(model, view).model_mapping()

    def is_validate(self, model, is_new):

        query = session.query(ChatRoomModel)\
            .filter((ChatRoomModel.id == model.id) | (ChatRoomModel.name == model.name))
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
        chat_room = None
        _id = req_data.get('id', None)
        if _id is not None:
            chat_room = session.query(ChatRoomModel).filter_by(id=_id).first()
        if chat_room is None:
            chat_room = ChatRoomModel()
        self.mapping(chat_room, req_data)
        if self.is_validate(chat_room, False if _id else True):
            session.add(chat_room)
            session.commit()
            return {'message': 'Saved Successfully', 'id': chat_room.id}
        else:
            raise Exception('Record already exists')

    def model(self, _id):
        return session.query(ChatRoomModel).filter_by(id=_id).first()

    def search(self, req_data):
        query = session.query(ChatRoomModel)
        if req_data and req_data.get('name') is not None:
            query = query.filter(ChatRoomModel.name.like('%' + req_data['name'] + '%'))
        data_list = query.limit(9999).all()
        return data_list