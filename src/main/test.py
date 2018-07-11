from flask import Blueprint, request, jsonify, json
from flasgger import swag_from

blueprint = Blueprint('test', __name__)

@swag_from('../../docs/test/test_get.yml')
@blueprint.route("/test", methods=['GET'])
def test_get():
    print(request.args)
    res = dict({'status': 1, 'data': {'message' : 'HelloWorld'}})
    return jsonify(res)

@swag_from('../../docs/test/test_post.yml')
@blueprint.route("/test", methods=['POST'])
def test_post():
    req_json = json.loads(request.data)
    res = dict({'status': 1, 'data': req_json})
    return jsonify(res)

