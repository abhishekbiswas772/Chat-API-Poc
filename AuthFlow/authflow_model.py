import base64
from db import db

class ChatUserDBModel(db.Model):
    __tablename__ = "db_chat_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    dob = db.Column(db.DateTime, nullable=False)
    profilePic = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password, email, dob, profilePic):
        self.username = username
        self.password = password
        self.email = email
        self.dob = dob
        self.profilePic = profilePic


class ChatUser:
    def __init__(self, username, password, email, dob, profile_pic):
        self.username = username
        self.password = password
        self.email = email
        self.dob = dob
        self.profile_pic = profile_pic

    @staticmethod
    def createBase64HashPassword(password):
        if (password is not None) and (password != ""):
            encoded_string = base64.b64encode(password.encode("utf-8"))
            return encoded_string
    
    @staticmethod
    def diChipherBase64HashPassword(password_hash):
        password = base64.b64decode(password_hash)
        return password
    
    def to_db_model(self):
        return ChatUserDBModel(
            username=self.username,
            password=self.password,
            email=self.email,
            dob=self.dob,
            profilePic=self.profile_pic
        )
    

