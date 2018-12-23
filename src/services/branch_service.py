from db import db, session
from utils.util import uid
from models.branch_model import BranchModel
from models.address_model import AddressModel
from models.img_model import ImgModel
from mappers.branch_mapper import BranchMapper
from mappers.address_mapper import AddressMapper
from mappers.img_mapper import ImgMapper
import datetime


class BranchService:

    session_info = None

    def mapping(self, model, view):
        print(self.session_info)
        if model.id is None:
            model.id = (self.session_info['vid']+'_'+view['name'].replace(" ", "_")).upper()[0:30]
            model.address = AddressModel()
            model.address.id = model.id
            model.img = ImgModel()
            model.img.id = model.id

        model.vid = self.session_info['vid']
        model.updatedBy = self.session_info['id']
        model.updatedOn = datetime.datetime.now()
        BranchMapper(model, view).model_mapping()
        AddressMapper(model.address, view.get('address', None)).model_mapping()
        ImgMapper(model.img, view.get('img', None)).model_mapping()

    def is_validate(self, model, is_new):
        model.vid = self.session_info['vid']
        query = session.query(BranchModel)\
            .filter(BranchModel.vid == model.vid)\
            .filter((BranchModel.mobile == model.mobile) | (BranchModel.email == model.email))
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

    def save(self, req_data):
        branch = None
        _id = req_data.get('id', None)
        if _id is not None:
            branch = session.query(BranchModel).filter_by(id=_id).first()
        if branch is None:
            branch = BranchModel()
        self.mapping(branch, req_data)
        if self.is_validate(branch, False if _id else True):
            session.add(branch)
            session.commit()
            return {'message': 'Saved Successfully', 'id': branch.id}
        else:
            raise Exception('Record already exists')

    def model(self, _id):
        return session.query(BranchModel).filter_by(id=_id).first()

    def search(self, req_data):
        print(req_data)
        query = session.query(BranchModel)
        query = query.filter(BranchModel.vid == self.session_info['vid'])
        if req_data and req_data.get('name') is not None:
            query = query.filter(BranchModel.name.like('%' + req_data['name'] + '%'))
        if req_data and req_data.get('mobile') is not None:
            query = query.filter(BranchModel.mobile.like('%' + req_data['mobile'] + '%'))
        data_list = query.limit(9999).all()
        print(data_list)
        return data_list
