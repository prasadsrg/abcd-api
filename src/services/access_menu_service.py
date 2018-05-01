from db import session
from models.access_menu_model import AccessMenuModel
from mappers.access_menu_mapper import AccessMenuMapper
import datetime

class AccessMenuService:

    session_info = None

    def mapping(self, model, view):
        model.vid = self.session_info['vid']
        model.updatedBy = self.session_info['id']
        model.updatedOn = datetime.datetime.now()
        AccessMenuMapper(model, view).model_mapping()

    def save(self, req_data):
        access_menu = None
        for item in req_data:
            _id = item.get('id', None)
            if _id is None:
                raise Exception('Not a valid record!')
            else:
                access_menu = session.query(AccessMenuModel).filter_by(id=_id).first()
            if access_menu is None:
                raise Exception('Not a valid record!')
            self.mapping(access_menu, item)
            session.add(access_menu)
        session.commit()
        return {'message': 'Saved Successfully', 'id': access_menu.id}


    def search(self, req_data):
        query = None
        if req_data:
            query = session.query(AccessMenuModel)\
                .filter(AccessMenuModel.vid == self.session_info['vid']) \
                .filter(AccessMenuModel.role == req_data['role'])
        else:
            query = session.query(AccessMenuModel)\
                .filter(AccessMenuModel.vid == self.session_info['vid'])

        data_list = query.all()
        return data_list
