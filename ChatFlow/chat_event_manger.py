from flask import Blueprint, request, jsonify, abort
from flask import session
from app import socketio
from RedisConfig.redis_manager import RedisManager
from flask_socketio import emit

blp = Blueprint("Chat Opeartions", __name__)
redis_manager = RedisManager()

@socketio.on('connect')
def handle_chat_user_connection():
    username = session.get('username')
    if username:
        redis_manager.add_user_connection(username, request.sid)
        print(f"{username} connected to SID {request.sid}")



@socketio.on('disconnect')
def handle_chat_user_disconnect():
    username = session.get('username')
    if username:
        redis_manager.remove_user_connections(username)
        redis_manager.makeUserOffline(username)
        print(f"{username} is disconnected")


@socketio.on('private_message')
def handle_private_message(data):
    recipient_username = data['reciver_username']
    message_to_send = data['message']
    sender_username = session.get('username')

    recipient_username_sid = redis_manager.get_user_connection(recipient_username)
    if recipient_username_sid:
        emit('private_message', {
            'sender' : sender_username,
            'message' :message_to_send
        }, room=recipient_username_sid.decode('utf-8'))
    else:
        emit('private_message', {
            'sender': 'system', 
            'message': 'User is offline'
        }, room=request.sid)
