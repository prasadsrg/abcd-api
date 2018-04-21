from db import db
from models.img_model import ImgModel
from models.address_model import AddressModel

class ConsumerModel(db.Model):
    __tablename__ = 'consumer'

    id = db.Column('id', db.String, primary_key=True)
    name = db.Column('name', db.String)
    mobile = db.Column('mobile', db.String)
    email = db.Column('email', db.String)
    aadhar = db.Column('aadhar', db.String)
    imgId = db.Column('img_id', db.String, db.ForeignKey('img.id'))
    img = db.relationship(ImgModel)
    addressId = db.Column('address_id', db.String, db.ForeignKey('address.id'))
    address = db.relationship(AddressModel)
    active = db.Column('active', db.Boolean)
    vid = db.Column('vid', db.String)
    createdOn = db.Column('created_on', db.DateTime)
    updatedBy = db.Column('updated_by', db.String)
    updatedOn = db.Column('updated_on', db.DateTime)