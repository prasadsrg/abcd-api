from flask import Blueprint
from flask import request, jsonify, json
from flask_jwt import jwt_required, current_identity
from flasgger import swag_from
from services.access_menu_service import AccessMenuService
from utils.util import model_to_dict

blueprint = Blueprint("access_menu", __name__)
access_menu_service = AccessMenuService()


@blueprint.route("/access_menu", methods=["POST"])
@jwt_required()
@swag_from('../../spec/access_menu/search.yml')
def access_menu_post():
    try:
        access_menu_service.session_info = current_identity
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        res_data = access_menu_service.search(req_data)
        res_json = {'status': 1, 'data': [model_to_dict(x) for x in res_data]}
    except Exception as e:
        print(e)
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)


@blueprint.route("/access_menu", methods=["PUT"])
@jwt_required()
@swag_from('../../spec/access_menu/save.yml')
def access_menu_put():
    try:
        access_menu_service.session_info = current_identity
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        res_data = access_menu_service.save(req_data)
        res_json = {'status': 1, 'data': res_data}
    except Exception as e:
        print(e)
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)





