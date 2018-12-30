from db import session
from utils.util import uid, model_to_dict
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
        print("==========================================================================")
        print(view)
        print("==========================================================================")

        if model.id is None:
            model.id = uid()
            model.room = ChatRoomModel()
            # model.room.id = uid()
            model.roomId = view["roomId"]
            # model.room.name = view["name"] if view["isIndividual"] is True else uid()
            # model.room.isIndividual = view["isIndividual"]
            model.profileId = view["profileId"]
            # model.chatMessage = ChatMessageModel()
            # model.chatMessage.id = uid()
            model.chatMessageId = view["messageId"]
            # model.chatMessage.message = view["chatMessage"]["message"]
            model.isView = True
        model.updatedBy = "SYSTEM"
        model.updatedOn = datetime.datetime.now()
        # ChatRoomMapper(model, view.get("room")).model_mapping()
        # ChatMessageMapper(model, view.get("chatMessage")).model_mapping()
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

    def model(self, _id):
        return session.query(ChatViewModel).filter_by(id=_id).first()

    def save(self, req_data):
        chat_view = None
        _id = req_data.get('id', None)
        if _id is not None:
            chat_view = session.query(ChatViewModel).filter_by(id=_id).first()
        if chat_view is None:
            chat_view = ChatViewModel()
        self.mapping(chat_view, req_data)
        if self.is_validate(chat_view, False if _id else True):
            session.add(chat_view)
            session.commit()
            return {'message': 'Saved Successfully', 'id': chat_view.id}
        else:
            raise Exception('Record already exists')

    def search(self, req_data):
        # query = session.query(ChatViewModel)
        if req_data.get("profileId") is not None and req_data.get('roomId') is not None:
            actualMessages = session.query(ChatMessageModel).filter(ChatMessageModel.roomId == req_data["roomId"]).count()
            viewedMessages = session.query(ChatViewModel).filter(
                ChatViewModel.roomId == req_data["roomId"],
                ChatViewModel.profileId == req_data["profileId"]
            ).count()
            data = actualMessages - viewedMessages
        return data