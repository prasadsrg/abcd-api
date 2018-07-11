from flask import Blueprint
from flask import request, jsonify, json
from flask_jwt import jwt_required, current_identity
from flasgger import swag_from
from services.app_data_service import AppDataService
from utils.util import model_to_dict


app_data_service = AppDataService()
blueprint = Blueprint("app_data", __name__)

@blueprint.route("/app_data", methods=["GET"])
@jwt_required()
@swag_from('../../spec/app_data/entity.yml')
def app_data_get():
    try:
        app_data_service.session_info = current_identity
        _id = request.args['id']
        res_data = app_data_service.model(_id)
        res_json = {'status': 1, 'data': model_to_dict(res_data)}
    except Exception as e:
        print(e)
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)

@blueprint.route("/app_data", methods=["POST"])
@jwt_required()
@swag_from('../../spec/app_data/search.yml')
def app_data_post():
    try :
        app_data_service.session_info = current_identity
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        res_data = app_data_service.search(req_data)
        res_json = {'status': 1, 'data': [model_to_dict(x) for x in res_data]}
    except Exception as e:
        print(e)
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)

@blueprint.route("/app_data", methods=["PUT"])
@jwt_required()
@swag_from('../../spec/app_data/save.yml')
def app_data_put():
    try :
        app_data_service.session_info = current_identity
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        res_data = app_data_service.save(req_data)
        res_json = {'status': 1, 'data': res_data}
    except Exception as e:
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)




