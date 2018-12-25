import os
from flask import Flask
from config import app_config
from flask_jwt import JWT
from flask_cors import CORS
import datetime
from configure import register, swagger
from utils.security_user import authenticate, identity
from main.websocket import socketio

def create_app():
    config_name = os.getenv('WEB_ENV', 'dev')
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(app_config[config_name])

    JWT.JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=99999999)
    app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=9999999)
    app.config['JWT_AUTH_URL_RULE'] = '/auth'
    jwt = JWT(app, authenticate, identity)
    register.register_blueprints(app)
    socketio.init_app(app)
    swagger.swagger(app)
    CORS(app)

    return app

app = create_app()

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    # app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
    socketio.run(app, host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])