from flask_smorest import Blueprint, abort
from flask import jsonify
from db import db
from flask.views import MethodView
from flask import request
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from RedisConfig.redis_manager import RedisManager

blp = Blueprint("Chat Flow", __name__, "Opeartions for chats")
redis_manager = RedisManager()

@blp.route("/chats/users")
class ChatRestManager(MethodView):
    def get(self):
        try:
            redis_chat_usr = []
            redis_list = redis_manager.get_online_users()
            for item in redis_list:
                redis_chat_usr.append(item.decode('utf-8'))
            return jsonify(
                {
                    "status" : True,
                    "data" : redis_chat_usr 
                }
            )
        except Exception as err:
            abort(500, message = {
                "status" : False,
                "message" : "Some Issue Occured"
            })
         
    def post(self):
        try:
            chat_data = request.json
            if chat_data.get("username") is not None:
                redis_manager.makeUserActive()
            else:
                abort(500, message = {
                    "status" : False,
                    "message" : "Some Issue Occured"
                })
        except Exception as err:
            abort(500, message = {
                "status" : False,
                "message" : "Some Issue Occured"
            })

    def put(self):
        try:
            chat_data = request.json
            if chat_data.get("username") is not None:
                redis_manager.makeUserOffline()
            else:
                abort(500, message = {
                    "status" : False,
                    "message" : "Some Issue Occured"
                })
        except Exception as err:
            abort(500, message = {
                "status" : False,
                "message" : "Some Issue Occured"
            })