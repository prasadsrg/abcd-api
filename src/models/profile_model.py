from db import db
from models.address_model import AddressModel
from models.img_model import ImgModel
from models.branch_model import BranchModel

class ProfileModel(db.Model):

    __tablename__ = 'profile'

    id = db.Column('id', db.String, primary_key=True)
    name = db.Column('name', db.String)
    mobile = db.Column('mobile', db.String)
    email = db.Column('email', db.String)
    aadhar = db.Column('aadhar', db.String)
    password = db.Column('password', db.String)
    token = db.Column('token', db.String)
    role = db.Column('role', db.String)
    addressId = db.Column('address_id', db.String, db.ForeignKey('address.id'))
    address = db.relationship(AddressModel)
    branchId = db.Column('branch_id', db.String, db.ForeignKey('branch.id'))
    branch = db.relationship(BranchModel)
    imgId = db.Column('img_id', db.String, db.ForeignKey('img.id'))
    img = db.relationship(ImgModel)
    active = db.Column('active', db.Boolean)
    vid = db.Column('vid', db.String)
    createdBy = db.Column('created_by', db.String)
    createdOn = db.Column('created_on', db.DateTime)
    updatedBy = db.Column('updated_by', db.String)
    updatedOn = db.Column('updated_on', db.DateTime)