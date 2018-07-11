from db import db
from db import session
from utils.util import uid
import json
import datetime
from models.vendor_model import VendorModel
from models.profile_model import ProfileModel
from models.branch_model import BranchModel
from models.address_model import AddressModel
from models.img_model import ImgModel
from mappers.vendor_mapper import VendorMapper
from mappers.branch_mapper import BranchMapper
from mappers.profile_mapper import ProfileMapper
from mappers.address_mapper import AddressMapper
from mappers.img_mapper import ImgMapper
class VendorService:

    session_info = None

    def profile_mapping(self, model, view):

        model.id = view['id']
        model.branchId = view['branch']['id']
        model.address = AddressModel()
        model.address.id = model.id
        model.address.vid = view['vid']
        model.img = ImgModel()
        model.img.id = model.id
        model.createdBy = "system"
        model.createdOn = datetime.datetime.now()
        model.vid = view['vid']
        model.updatedBy = "system"
        model.updatedOn = datetime.datetime.now()

        ProfileMapper(model, view).model_mapping()
        AddressMapper(model.address, view.get('address')).model_mapping()
        ImgMapper(model.img, view.get('img')).model_mapping()

    def branch_mapping(self, model, view):

        model.id = view['id']
        model.address = AddressModel()
        model.address.id = model.id
        model.img = ImgModel()
        model.img.id = model.id

        model.vid = view['vid']
        model.updatedBy = view['id']
        model.updatedOn = datetime.datetime.now()
        BranchMapper(model, view).model_mapping()
        AddressMapper(model.address, view.get('address', None)).model_mapping()
        ImgMapper(model.img, view.get('img', None)).model_mapping()

    def model(self, _id):
        return session.query(VendorModel).filter_by(id=_id).first()

    def save(self, req_data):
        vendor = None

        req_data["branch"]["id"] = req_data["id"] + "_MAIN_BRANCH"
        req_data["branch"]["vid"] = req_data["id"]
        req_data["branch"]["address"]["id"] = req_data["branch"]["id"]
        req_data["branch"]["img"]["id"] = req_data["branch"]["id"]
        req_data["profile"]["id"] = req_data["id"]+"_MAIN_PROFILE"
        req_data["profile"]["vid"] = req_data["id"]
        req_data["profile"]["role"] = "SUPER_ADMIN"
        req_data["profile"]["branch"]["vid"] = req_data["branch"]["vid"]
        req_data["profile"]["img"]["id"] = req_data["profile"]["id"]
        req_data["profile"]["address"]["id"] = req_data["profile"]["id"]

        if req_data.get('id', None) is not None:
           vendor = VendorModel.query.filter_by(id=req_data.get('id')).first()
        if vendor is None:
            vendor = VendorModel()

        VendorMapper(vendor, req_data).model_mapping()
        db.session.add(vendor)
        db.session.commit()

        profile = ProfileModel()
        self.profile_mapping(profile, req_data["profile"])
        session.add(profile)
        session.commit()

        branch = BranchModel()
        self.branch_mapping(branch, req_data['branch'])
        session.add(branch)
        session.commit()

        return {'message': 'Saved Successfully', 'id': req_data['id']}

    def search(self, req_data):
        print(req_data)
        query = session.query(VendorModel)
        query = query.filter(VendorModel.id == self.session_info['vid'])
        if req_data and req_data.get('name') is not None:
            query = query.filter(VendorModel.name.like('%' + req_data['name'] + '%'))
        if req_data and req_data.get('mobile') is not None:
            query = query.filter(VendorModel.mobile.like('%' + req_data['mobile'] + '%'))
        data_list = query.limit(9999).all()
        print(data_list)
        return data_list