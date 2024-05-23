from flask_smorest import Blueprint, abort
from flask import jsonify, session
from db import db
from flask.views import MethodView
from flask import request
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from AuthFlow.authflow_model import ChatUser, ChatUserDBModel
from uploads.upload_manager import UploadManager

blp = Blueprint("Auth Flow", __name__, "Operations for Auth Flow")

class AuthRestManager(MethodView):
    @blp.route("/chats/auth/get_all_users")
    def get(self):
        try:
            all_chat_user = ChatUserDBModel.query.all()
            return jsonify({
                "status" : True,
                "message" : all_chat_user
            }), 200
        except SQLAlchemyError or IntegrityError as err:
            print(err)
            abort(500, message = {
                "status" : False,
                "message" : "Some Issue Happended"
            })
        except Exception as e:
            print(err)
            abort(500, message = {
                "status" : False,
                "message" : "Some Issue Happened"
            })

    @blp.route("/chats/auth/create_user")
    def post(self):
        auth_data = request.json
        if not auth_data:
            abort(400, message = "No Data Provided")
        else:
            cUser = ChatUser()
            id = auth_data.get("userid")
            username = auth_data.get("username")
            password = auth_data.get("password")
            email = auth_data.get("email")
            dob = auth_data.get("dob")
            profile_image = auth_data.get("profile_image") 
            try:
                uploadManager = UploadManager()
                result_from_upload_minio = uploadManager.postImageUpload(profile_image)
                if result_from_upload_minio:
                    getImageUrl = uploadManager.getImageUploadURL(username+".jpeg")
                    cUser.username = username
                    cUser.id = id
                    cUser.password = ChatUser.createBase64HashPassword(password)
                    cUser.dob = dob
                    cUser.email = email
                    cUser.profile_pic = getImageUrl 
                    chatDbModel = cUser.to_db_model()
                    db.session.add(chatDbModel)
                    db.session.commit()
                    return jsonify({
                        "status" : True, 
                        "message": auth_data
                    }), 201
                else:
                    abort(500, message = {
                        "status" : False,
                        "message" : "Some Error Occured"
                    })
            except SQLAlchemyError or IntegrityError as err:
                print(err)
                abort(500, message = {
                    "status" : False,
                    "message" : "Some Error Occured"
                })
            except Exception as err:
                print(err)
                print(err)
                abort(500, message = {
                    "message" : "Some Error Occured"
                })
    @blp.route("/chats/auth/get_single_user/<string:user_id>")
    def get(self, user_id):
        try:
            user = ChatUserDBModel.query.get(user_id)
            if user:
                return jsonify({
                    "status": True,
                    "message": user
                }), 200
            else:
                return jsonify({
                    "status": False,
                    "message": "User not found"
                }), 404
        except SQLAlchemyError or IntegrityError as err:
            print(err)
            abort(500, message={
                "status": False,
                "message": "Some Issue Happened"
            })
        except Exception as e:
            print(e)
            abort(500, message={
                "status": False,
                "message": "Some Issue Happened"
            })


class AuthLoginRestManager(MethodView):
    @blp.route('/chat/auth/login')
    def post(self):
        try:
            user_data = request.json
            username = user_data.get("username")
            password = user_data.get("password")
            if username is None and password is None and username == "" and password == "":
                abort(400, {
                    "status" : False,
                    "message" : "Insuffient data found"
                })
            probable_user = ChatUserDBModel.query.filter_by(username=username).first()
            if probable_user:
                if probable_user.username != username:
                    abort(400, {
                        "status" : False,
                        "message" : "username is incorrect"
                    })
                get_passoword_de_cipher = ChatUser.diChipherBase64HashPassword(probable_user.password)
                if password != get_passoword_de_cipher:
                    abort(400, {
                        "status" : False,
                        "message" : "password is incorrect"
                    })
                session['username'] = username
            else:
                abort(400, {
                    "status" : False,
                    "message" : "User not exists"
                })
        except SQLAlchemyError or IntegrityError or Exception as err:
            print(err)
            abort(
                500, message = {
                    'status' : False,
                    'message' : "Some Issue Occured"
                }
            )
    

