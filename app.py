import eventlet
eventlet.monkey_patch()
import os
from flask import Flask
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_smorest import Api
from db import db
from AuthFlow.auth_flow import blp as AuthBlueprint
from ChatFlow.chat_manger import blp as ChatEventBlueprints


app = Flask(__name__)
app.config["API_VERSION"] = os.getenv("API_VERSION", "v1")
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Chapter API's"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)
api.register_blueprint(AuthBlueprint)
api.register_blueprint(ChatEventBlueprints)
socketio = SocketIO(app, cors_allowed_origins="*")
app.app_context().push()
db.init_app(app)
migrate = Migrate(app, db)

if __name__ == "__main__":
    print("Rest API and Socket Running")
    socketio.run(app, port=5000, host='0.0.0.0')
