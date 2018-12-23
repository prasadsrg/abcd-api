from db import session
from utils.util import uid
from models.chat_message_model import ChatMessageModel
from models.chat_room_model import ChatRoomModel
from models.chat_view_model import ChatViewModel
from mappers.chat_room_mapper import ChatRoomMapper
from mappers.chat_message_mapper import ChatMessageMapper
from mappers.chat_view_mapper import ChatViewMapper
import datetime


class ChatViewService:

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
            model.chatMessage = ChatMessageModel()
            model.chatMessage.id = uid()
            model.chatMessageId = model.chatMessage.id
            model.chatMessage.message = view["chatMessage"]["message"]
            model.isView = True
        model.updatedBy = self.session_info["name"] if self.session_info.get("name") else "SYSTEM"
        model.updatedOn = datetime.datetime.now()
        ChatRoomMapper(model, view.get("room")).model_mapping()
        ChatMessageMapper(model, view.get("chatMessage")).model_mapping()
        ChatViewMapper(model, view).model_mapping()

    def is_validate(self, model, is_new):

        query = session.query(ChatViewModel)\
            .filter(
            ChatViewModel.profileId == model.profileId,
            ChatViewModel.roomId == model.roomId,
            ChatViewModel.chatMessageId == model.chatMessageId
        )
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
        chat_message = None
        _id = req_data.get('id', None)
        if _id is not None:
            chat_message = session.query(ChatViewModel).filter_by(id=_id).first()
        if chat_message is None:
            chat_message = ChatViewModel()
        self.mapping(chat_message, req_data)
        if self.is_validate(chat_message, False if _id else True):
            session.add(chat_message)
            session.commit()
            return {'message': 'Saved Successfully', 'id': chat_message.id}
        else:
            raise Exception('Record already exists')

    def model(self, _id):
        return session.query(ChatViewModel).filter_by(id=_id).first()

    def search(self, req_data):
        query = session.query(ChatViewModel)
        query = query.filter(ChatViewModel.profileId == self.session_info['profileId'])
        if req_data and req_data.get('name') is not None:
            query = query.filter(ChatViewModel.name.like('%' + req_data['name'] + '%'))
        data_list = query.limit(9999).all()
        return data_list