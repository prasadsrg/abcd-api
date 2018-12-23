from db import db
from db import session
from utils.util import uid
from models.app_data_model import AppDataModel
from mappers.app_data_mapper import AppDataMapper
import datetime


class AppDataService:
    session_info = None

    def mapping(self, model, view):
        if model.id is None:
            view['data'] = view['name'].upper()
            model.id = (view['code']+'_'+view['data'])[0:30]

        model.vid = self.session_info['vid']
        model.updatedBy = self.session_info['id']
        model.updatedOn = datetime.datetime.now()
        AppDataMapper(model, view).model_mapping()

    def is_validate(self, model, is_new):

        model.vid = self.session_info['vid']
        query = session.query(AppDataModel)
        query = query.filter(AppDataModel.vid == model.vid)
        query = query.filter(AppDataModel.name == model.name)
        query = query.filter(AppDataModel.code == model.code)
        data_list = query.all()
        print(data_list)
        if data_list:
            if is_new:
                return False
            else:
                for item in data_list:
                    if item.id != model.id:
                        return False
        return True

    def model(self, _id):
        return session.query(AppDataModel).filter_by(id=_id).first()

    def save(self, req_data):
        app_data = None
        _id = req_data.get('id', None)
        if _id is None:
            app_data = AppDataModel()
        else:
            app_data = session.query(AppDataModel).filter_by(id=_id).first()
        self.mapping(app_data, req_data)
        if self.is_validate(app_data, False if _id else True):
            session.add(app_data)
            session.commit()
            return {'message': 'Saved Successfully', 'id': app_data.id}
        else:
            raise Exception('Record already exists')

    def search(self, req_data):
        query = None
        if req_data and req_data.get('code') is not None:
            query = session.query(AppDataModel)
            query = query.filter(AppDataModel.vid == self.session_info['vid'])
            query = query.filter(AppDataModel.code == req_data['code'])
        else:
            query = session.query(AppDataModel)
            query = query.filter(AppDataModel.vid == self.session_info['vid'])

        data_list = query.all()
        return data_list