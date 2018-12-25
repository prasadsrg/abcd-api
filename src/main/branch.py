from flask import Blueprint
from flask import request, jsonify, json
from flask_jwt import jwt_required, current_identity
from flasgger import swag_from
from services.branch_service import BranchService
from utils.util import model_to_dict

blueprint = Blueprint("branch", __name__)
branch_service = BranchService()

@blueprint.route("/branch", methods=["PUT"])
@jwt_required()
@swag_from('../../spec/branch/save.yml')
def branch_put():
    try:
        branch_service.session_info = current_identity
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        res_data = branch_service.save(req_data)
        res_json = {'status': 1, 'data': res_data}
    except Exception as e:
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)

@blueprint.route("/branch", methods=["POST"])
@jwt_required()
@swag_from('../../spec/branch/search.yml')
def branch_post():
    try:
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        print(req_data)
        branch_service.session_info = current_identity
        res_data = branch_service.search(req_data)
        print(res_data)
        res_json = {'status': 1, 'data': [model_to_dict(x) for x in res_data ]}
        print(res_json)
    except Exception as e:
        print(e)
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)

@blueprint.route("/branch", methods=["GET"])
@jwt_required()
@swag_from('../../spec/branch/entity.yml')
def branch_get():
    try:
        branch_service.session_info = current_identity
        _id = request.args['id']
        res_data = branch_service.model(_id)
        res_json = {'status': 1, 'data': model_to_dict(res_data)}
    except Exception as e:
        print(e)
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)
