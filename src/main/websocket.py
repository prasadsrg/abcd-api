from flask_socketio import SocketIO, join_room, leave_room, close_room, emit
from flask_jwt import jwt_required, current_identity
from flask import Blueprint, jsonify, session, request, json
from services.chat_user_service import ChatUserService
from services.chat_room_service import ChatRoomService
from services.chat_message_service import ChatMessageService
from services.chat_view_service import ChatViewService

socketio = SocketIO()

blueprint = Blueprint("websocket", __name__)
chat_user_service = ChatUserService()
chat_room_service = ChatRoomService()
chat_message_service = ChatMessageService()
chat_view_service = ChatViewService()


@socketio.on('join')
def join(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = message.get('room')
    join_room(room)
    user = {'msg': message.get('name') + ' has entered the room.', "room": room}
    emit('join', {'msg': message.get('name') + ' has entered the room.'}, room=room, callback=message_received(user))


@socketio.on('text')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = message.get('room')
    user = {"name": message.get('name'), "message": message['msg'], "room": room}
    print(request.remote_addr)
    emit('text', {"name": message.get('name'), 'msg': message['msg']}, room=room, callback=message_received(user))


@socketio.on('left')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = message.get('room')
    leave_room(room)
    user = {'msg': message.get('name') + ' has left the room.'}
    emit('left', {'msg': message.get('name') + ' has left the room.'}, room=room, callback=message_received(user))


def message_received(json):
    print(json)
    pass


@blueprint.route("/adduser", methods=["PUT"])
def add_user():
    try:
        # chat_user_service.session_info = current_identity
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        if req_data["isIndividual"] == True and req_data.get("roomId") is None:
            req_data["profileId"] = req_data["senderId"]
            res_data = chat_user_service.save(req_data)
            req_data["profileId"] = req_data["recieverId"]
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
def create_room():
    try:
        # chat_user_service.session_info = current_identity
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
def get_rooms():
    try:
        # chat_user_service.session_info = current_identity
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
def get_messages():
    try:
        # chat_user_service.session_info = current_identity
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
def unread_messages():
    try:
        # chat_user_service.session_info = current_identity
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

