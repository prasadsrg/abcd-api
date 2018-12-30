from flask_socketio import SocketIO, join_room, leave_room, close_room, emit
from flask_jwt import jwt_required, current_identity
from flask import Blueprint, jsonify, session, request, json
from services.chat_user_service import ChatUserService
from services.chat_room_service import ChatRoomService
from services.chat_message_service import ChatMessageService
from services.chat_view_service import ChatViewService
from flasgger import swag_from

socketio = SocketIO()

blueprint = Blueprint("websocket", __name__)
chat_user_service = ChatUserService()
chat_room_service = ChatRoomService()
chat_message_service = ChatMessageService()
chat_view_service = ChatViewService()

data = []

@socketio.on('join')
def join(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    print(message)
    room = message.get('roomId')
    join_room(room)
    data.append((room, message.get("profileId")))
    print(set(data))
    res_data = {'msg': message.get('profileId', "") + ' has entered the room.', "room": room}
    emit('join', {'msg': message.get('profileId') + ' has entered the room.'}, room=room, callback=user_joined(res_data))


@socketio.on('text')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    print(message)
    room = message.get('roomId')
    user = {"profileId": message.get('profileId'), "message": message['message'], "roomId": room}
    print(request.remote_addr)
    res_data = {"roomId": room, "message": message["message"], "profileId": message.get('profileId')}
    print(res_data)
    print(set(data))
    emit('text', {"profileId": message.get('profileId'), 'message': message['message']}, room=room, callback=message_received(res_data))


@socketio.on('left')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    print(message)
    room = message.get('roomId')
    leave_room(room)
    print(set(data))
    data.remove((room, message["profileId"]))
    res_data = {'msg': message.get('profileId') + ' has left the room.'}
    emit('left', {'msg': message.get('profileId') + ' has left the room.'}, room=room, callback=user_left(res_data))


def message_received(req_data):
    # try:
    messages = chat_message_service.save(req_data)
    messageId = messages["id"]
    print(set(data))
    for item in set(data):
        if item[0] == req_data["roomId"]:
            view_data = {"roomId": req_data["roomId"], "messageId": messageId, "profileId": item[1]}
            chat_view_service.save(view_data)
        else:
            print(item)
    # except Exception as e:
    #     print(e)


def user_joined(req_data):
    try:
        print(req_data)
    except Exception as e:
        print(e)


def user_left(req_data):
    try:
        print(req_data)
    except Exception as e:
        print(e)


@blueprint.route("/adduser", methods=["PUT"])
# @jwt_required()
@swag_from('../../spec/chatuser/save.yml')
def add_user():
    try:
        chat_user_service.session_info = current_identity
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        if req_data["isIndividual"] == True:
            req_data["userId"] = req_data["senderId"]
            res_data = chat_user_service.save(req_data)
            req_data["userId"] = req_data["receiverId"]
            res_json = {'status': 1, 'data': res_data}
        else:
            res_data = chat_user_service.save(req_data)
            res_json = {'status': 1, 'data': res_data}
    except Exception as e:
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)


@blueprint.route("/createroom", methods=["PUT"])
# @jwt_required()
@swag_from('../../spec/chatroom/save.yml')
def create_room():
    try:
        chat_room_service.session_info = current_identity
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        res_data = chat_room_service.save(req_data)
        res_json = {'status': 1, 'data': res_data}
    except Exception as e:
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)


@blueprint.route("/getrooms", methods=["POST"])
# @jwt_required()
@swag_from('../../spec/chatuser/search.yml')
def get_rooms():
    # try:
    chat_user_service.session_info = current_identity
    req_json = json.loads(request.data)
    req_data = req_json.get('data', None)
    res_data = chat_user_service.search(req_data)
    res_json = {'status': 1, 'data': res_data}
    # except Exception as e:
    #     if e.args:
    #         res_data = e.args[0]
    #     else:
    #         res_data = e
    #     res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)

@blueprint.route("/getroom", methods=["POST"])
# @jwt_required()
@swag_from('../../spec/chatuser/search.yml')
def get_room():
    try:
        chat_user_service.session_info = current_identity
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        res_data = chat_user_service.search(req_data)
        res_json = {'status': 1, 'data': res_data}
    except Exception as e:
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)

@blueprint.route("/getmessages", methods=["POST"])
# @jwt_required()
@swag_from('../../spec/chatmessages/search.yml')
def get_messages():
    try:
        chat_user_service.session_info = current_identity
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        res_data = chat_message_service.search(req_data)
        res_json = {'status': 1, 'data': res_data}
    except Exception as e:
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)


@blueprint.route("/unreadmessages", methods=["POST"])
# @jwt_required()
@swag_from('../../spec/chatview/search.yml')
def unread_messages():
    try:
        chat_user_service.session_info = current_identity
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        res_data = chat_view_service.search(req_data)
        res_json = {'status': 1, 'data': res_data}
    except Exception as e:
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)
