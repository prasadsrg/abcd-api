from flask import Blueprint, request, jsonify, json
from flask_jwt import jwt_required, current_identity
from flasgger import swag_from
from services.access_data_service import AccessDataService
from utils.util import model_to_dict

blueprint = Blueprint("access_data", __name__)
access_data_service = AccessDataService()


@blueprint.route("/access_data", methods=["POST"])
@jwt_required()
@swag_from('../../spec/access_data/search.yml')
def access_data_post():
    try:
        access_data_service.session_info = current_identity
        print("--------------------------")
        print(current_identity)
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        res_data = access_data_service.search(req_data)
        res_json = {'status': 1, 'data': [model_to_dict(x) for x in res_data]}
        print(res_json)
    except Exception as e:
        print(e)
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)