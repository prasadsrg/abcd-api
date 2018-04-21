from db import db
from models.address_model import AddressModel
from models.img_model import ImgModel
class BranchModel(db.Model):

    __tablename__ = 'branch'

    id = db.Column('id', db.String, primary_key=True)
    name = db.Column('name', db.String)
    phone = db.Column('phone', db.String)
    mobile = db.Column('mobile', db.String)
    email = db.Column('email', db.String)
    pan = db.Column('pan', db.String)
    tan = db.Column('tan', db.String)
    lat = db.Column('lat', db.String)
    lng = db.Column('lng', db.String)
    isMain = db.Column('is_main', db.Boolean)
    active = db.Column('active', db.Boolean)
    vid = db.Column('vid', db.String)
    addressId = db.Column('address_id', db.String, db.ForeignKey('address.id'))
    address = db.relationship(AddressModel)
    imgId = db.Column('img_id', db.String, db.ForeignKey('img.id'))
    img = db.relationship(ImgModel)
    updatedBy = db.Column('updated_by', db.String)
    updatedOn = db.Column('updated_on', db.DateTime)