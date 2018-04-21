from flask import request, jsonify, json
from flask_restful import  Resource
from flask_jwt import jwt_required, current_identity
from flasgger import swag_from

from services.profile_service import ProfileService
from utils.util import model_to_dict

class ProfileResource (Resource):

    profile_service = ProfileService()

    @jwt_required()
    @swag_from('../../spec/profile/save.yml')
    def put(self):
        try :
            self.profile_service.session_info = current_identity
            req_json = json.loads(request.data)
            req_data = req_json.get('data', None)
            print(req_data)
            res_data = self.profile_service.save(req_data)
            res_json = {'status': 1, 'data': res_data}
        except Exception as e:
            if e.args:
                res_data = e.args[0]
            else:
                res_data = e
            res_json = {'status': 0, 'error': res_data}
        return jsonify(res_json)

    @jwt_required()
    @swag_from('../../spec/profile/search.yml')
    def post(self):
        try:
            req_json = json.loads(request.data)
            req_data = req_json.get('data', None)
            self.profile_service.session_info = current_identity
            res_data = self.profile_service.search(req_data)
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

    @jwt_required()
    @swag_from('../../spec/profile/entity.yml')
    def get(self):
        try:
            self.profile_service.session_info = current_identity
            _id = request.args['id']
            res_data = self.profile_service.model(_id)
            res_json = {'status': 1, 'data': model_to_dict(res_data)}
        except Exception as e:
            print(e)
            if e.args:
                res_data = e.args[0]
            else:
                res_data = e
            res_json = {'status': 0, 'error': res_data}
        return jsonify(res_json)

    @jwt_required()
    @swag_from('../../spec/profile/delete.yml')
    def delete(self):
        self.profile_service.session_info = current_identity
        id = request.args['id']
        req_data = {'id': id, 'active': False}
        res_data = self.profile_service.save(req_data)
        print(res_data)
        # return { 'status': 1, data : list(map( lambda x: x.json(), ItemModel.query.all() ) ) }
        # return { 'status': 1, data : [x.json for x in ItemModel.query.all() ] }
        return {'status': 1, 'message': 'Deleted successfully'}
