# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from mongoengine import connect
from instance.config import Config
from flask_socketio import SocketIO
from flask_cors import CORS
# local import
from instance.config import app_config

# initialize sql-alchemy, socket and mongo
db = SQLAlchemy()  # postgres
connect('garbage-db', host=Config.MONGO_URI)  # mongo engine connection
socketio = SocketIO()

from routes.User import router as user_router
from routes.garbageCan import router as garbage_can_router
from routes.company import router as company_router
from routes.driver import router as driver_router
from socketHandler.index import socketio as socket_handler


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=False)
    CORS(app)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('../instance/config.py')
    app.register_blueprint(user_router, url_prefix="/api/user")
    app.register_blueprint(garbage_can_router, url_prefix="/api/garbage")
    app.register_blueprint(company_router, url_prefix="/api/company")
    app.register_blueprint(driver_router, url_prefix="/api/driver")

    socketio.init_app(app)
    # socketio.run(app, port=5000, debug=True, use_reloader=True)

    socket_handler.init_io(socketio)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app
