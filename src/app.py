from flask import Flask, request
from flask_jwt import JWT
from flask_restful import Api
from config import app_config
from flasgger import Swagger
import os
import datetime

config_name = os.getenv('WEB_ENV', 'dev')
app = Flask(__name__, instance_relative_config=False)
api = Api(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response


app.config.from_object(app_config[config_name])

from utils.security_user import SecurityUser

JWT.JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=99999999)
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=9999999)
jwt = JWT(app, SecurityUser.authenticate, SecurityUser.identity)

api.add_resource(SecurityUser, '/auth')

from resources.vendor_resource import VendorResource
api.add_resource(VendorResource, '/vendor')

from resources.branch_resource import BranchResource
api.add_resource(BranchResource, '/branch')


from resources.consumer_resource import ConsumerResource
api.add_resource(ConsumerResource, '/consumer')


from resources.profile_resource import ProfileResource
api.add_resource(ProfileResource, '/profile')

from resources.access_menu_resource import AccessMenuResource
api.add_resource(AccessMenuResource, '/access_menu')

from resources.access_data_resource import AccessDataResource
api.add_resource(AccessDataResource, '/access_data')

from resources.app_data_resource import AppDataResource
api.add_resource(AppDataResource, '/app_data')

from resources.data_load_resource import DataLoadResource
api.add_resource(DataLoadResource, '/data_load')

from resources.data_report_resource import DataReportResource
api.add_resource(DataReportResource, '/reports/download/monthly')

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', "Authorization, Content-Type")
#     response.headers.add('Access-Control-Expose-Headers', "Authorization")
#     response.headers.add('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS")
#     response.headers.add('Access-Control-Allow-Credentials', "true")
#     response.headers.add('Access-Control-Max-Age', 60 * 60 * 24 * 20)
#     return response

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#     return response
    # if request.method == 'OPTIONS':
    #     response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
    #     headers = request.headers.get('Access-Control-Request-Headers')
    #     if headers:
    #         response.headers['Access-Control-Allow-Headers'] = headers
    # header = request.headers.get('Authorization')
    # if header:
    #     _, token = header.split()
    #     request.identity = SecurityUser.identity(jwt.jwt_decode_callback(token))
    #     print(request.identity)
    # return response

if __name__ == '__main__':
    app.config['SWAGGER'] = {
        "swagger_version": "2.0",
        "title": "ABCD",
        "headers": [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE"),
            ('Access-Control-Allow-Credentials', "true"),
        ],
    }
    # Swagger(app, template={
    #     "swagger": "3.0",
    #     "consumes": [
    #         "application/json",
    #         "application/x-www-form-urlencoded",
    #     ],
    #     "produces": [
    #         "application/json",
    #     ],
    #     "securityDefinitions": {
    #         "jwt": {
    #             "type": 'apiKey',
    #             "name": 'Authorization',
    #             "in": 'header'
    #         }
    #     },
    #     "security": [
    #         {"jwt": []}
    #     ]
    # },)
    swagger_config = {
        'specs': [
            {
                'endpoint': 'apispec',
                'route': '/apispec.json',
                'rule_filter': lambda rule: True,
                'model_filter': lambda tag: False,
            }
        ],
        'swagger_ui': False,
    }
    Swagger(app, config=swagger_config, template={
        "swagger": "3.0",
        "headers": [
        ],
        "consumes": [
            "application/json",
            "application/x-www-form-urlencoded",
        ],
        "produces": [
            "application/json",
        ],
        "securityDefinitions": {
            "jwt": {
                "type": 'apiKey',
                "name": 'Authorization',
                "in": 'header'
            }
        },
        "security": [
            {"jwt": []}
        ]

    })

    from db import db
    db.init_app(app)
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])