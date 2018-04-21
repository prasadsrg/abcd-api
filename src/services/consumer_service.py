from db import db
from db import session
from utils.util import uid
from models.consumer_model import ConsumerModel
from models.img_model import ImgModel
from mappers.consumer_mapper import ConsumerMapper
from mappers.img_mapper import ImgMapper
from models.address_model import AddressModel
from mappers.address_mapper import AddressMapper
import datetime

class ConsumerService:

    session_info = None

    def mapping(self, model, view):
        print(self.session_info)
        if model.id is None:
            model.id = uid()
            model.address = AddressModel()
            model.address.id = model.id
            model.img = ImgModel()
            model.img.id = model.id
            model.createdOn = datetime.datetime.now()

        model.vid = self.session_info['vid']
        model.updatedBy = self.session_info['id']
        model.updatedOn = datetime.datetime.now()

        ConsumerMapper(model, view).model_mapping()
        AddressMapper(model.address, view.get('address', None)).model_mapping()
        ImgMapper(model.img, view.get('img', None)).model_mapping()
        return model

    def is_validate(self, model, is_new):
        model.vid = self.session_info['vid']
        query = session.query(ConsumerModel)\
            .filter(ConsumerModel.vid == model.vid)\
            .filter((ConsumerModel.mobile == model.mobile))
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
        return session.query(ConsumerModel).filter_by(id=_id).first()

    def save(self, req_data):

        consumer = None
        _id = req_data.get('id', None)
        print(_id)
        if _id is not None:
            consumer = session.query(ConsumerModel).filter_by(id=_id).first()
        if consumer is None:
            consumer = ConsumerModel()

        self.mapping(consumer, req_data)
        if self.is_validate(consumer, False if _id else True):
            session.add(consumer)
            session.commit()
            return {'message': 'Saved Successfully', 'id': consumer.id}
        else:
            raise Exception('Record already exists')


    def search(self, req_data):
        print(req_data)
        query = session.query(ConsumerModel)
        query = query.filter(ConsumerModel.vid == self.session_info['vid'])
        if req_data and req_data.get('name') is not None:
            query = query.filter(ConsumerModel.name.like('%' + req_data['name'] + '%'))
        if req_data and req_data.get('mobile') is not None:
            query = query.filter(ConsumerModel.mobile.like('%' + req_data['mobile'] + '%'))
        data_list = query.limit(9999).all()
        print(data_list)
        return data_list