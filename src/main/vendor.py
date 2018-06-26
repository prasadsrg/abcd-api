from flask import Blueprint
from flask import request, jsonify, json
from flask_jwt import jwt_required, current_identity
from flasgger import swag_from
from services.vendor_service import VendorService
from utils.util import model_to_dict

blueprint = Blueprint("vendor_resource", __name__)
vendor_service = VendorService()


@blueprint.route("/vendor", methods=["PUT"])
@jwt_required()
@swag_from('../../spec/vendor/save.yml')
def vendor_put():
    try :
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        res_data = vendor_service.save(req_data)
        res_json = {'status': 1, 'data': res_data}
    except Exception as e:
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)


@blueprint.route("/vendor", methods=["POST"])
@jwt_required()
@swag_from('../../spec/vendor/search.yml')
def vendor_post():
    try:
        vendor_service.session_info = current_identity
        req_json = json.loads(request.data)
        req_data = req_json.get('data', None)
        res_data = vendor_service.search(req_data)
        print(res_data)
        res_json = {'status': 1, 'data': [ model_to_dict(x) for x in res_data ]}
        print(res_json)
    except Exception as e:
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)


@blueprint.route("/vendor", methods=["GET"])
@jwt_required()
@swag_from('../../spec/vendor/entity.yml')
def vendor_get():
    try:
        vendor_service.session_info = current_identity
        _id = request.args['id']
        res_data = vendor_service.model(_id)
        res_json = {'status': 1, 'data': model_to_dict(res_data)}
    except Exception as e:
        print(e)
        if e.args:
            res_data = e.args[0]
        else:
            res_data = e
        res_json = {'status': 0, 'error': res_data}
    return jsonify(res_json)
