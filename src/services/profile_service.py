from db import session
from utils.util import uid
from models.profile_model import ProfileModel
from models.address_model import AddressModel
from models.img_model import ImgModel

from mappers.profile_mapper import ProfileMapper
from mappers.img_mapper import ImgMapper
from mappers.address_mapper import AddressMapper
import datetime


class ProfileService:

    session_info = None

    def mapping(self, model, view):

        if model.id is None:
            model.id = uid()
            model.branchId = view['branch']['id']
            model.address = AddressModel()
            model.address.id = model.id
            model.address.vid = self.session_info['vid']
            model.img = ImgModel()
            model.img.id = model.id
            model.createdBy = self.session_info['id']
            model.createdOn = datetime.datetime.now()

        model.vid = self.session_info['vid']
        model.updatedBy = self.session_info['id']
        model.updatedOn = datetime.datetime.now()

        ProfileMapper(model, view).model_mapping()
        AddressMapper(model.address, view.get('address')).model_mapping()
        ImgMapper(model.img, view.get('img')).model_mapping()

    def is_validate(self, model, is_new):
        model.vid = self.session_info['vid']
        query = session.query(ProfileModel)\
            .filter(ProfileModel.vid == model.vid)\
            .filter((ProfileModel.mobile == model.mobile) | (ProfileModel.email == model.email))
        data_list = query.all()
        if data_list:
            if is_new:
                print("true")
                return False
            else:
                for item in data_list:
                    print("item", item)
                    if item.id != model.id:
                        print("item.id", item.id)
                        print("model.id", model.id)
                        return False
        return True
    def model(self, _id):
        return session.query(ProfileModel).filter_by(id=_id).first()


    def save(self, req_data):

        profile = None
        _id = req_data.get('id')
        if _id is not None:
            profile = self.model(_id)
        if profile is None:
            profile = ProfileModel()

        self.mapping(profile, req_data)
        if self.is_validate(profile, False if _id else True):
            session.add(profile)
            session.commit()
            return {'message': 'Saved Successfully', 'id': profile.id}
        else:
            raise Exception('Record already exists')

    def search(self, req_data):

        query = session.query(ProfileModel)
        query = query.filter(ProfileModel.vid == self.session_info['vid'])
        if req_data and req_data.get('name') is not None:
            query = query.filter(ProfileModel.name.like('%'+req_data['name']+'%'))
        if req_data and req_data.get('mobile') is not None:
            query = query.filter(ProfileModel.mobile.like('%'+req_data['mobile']+'%'))
        data_list = query.limit(9999).all()
        filter_list = list(filter((lambda x: x.role != 'SUPER_ADMIN'), data_list))
        return filter_list
