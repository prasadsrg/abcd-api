from db import session, db
from sqlalchemy import text
from models.access_data_model import AccessDataModel
from mappers.access_data_mapper import AccessDataMapper
import datetime


class AccessDataService:
    session_info = None

    def search(self, req_data):
        query = None
        if req_data:
            query = session.query(AccessDataModel)\
                .filter(AccessDataModel.code == req_data['code'])
        else:
            query = session.query(AccessDataModel)

        data_list = query.all()
        filter_list = list(filter((lambda x: x.val != 'SUPER_ADMIN'), data_list))
        return filter_list

    def dataload(self, results):
        returnVal = []
        for result in results:
            data = {'id': result[0], 'name': result[1]};
            returnVal.append(data)
        return returnVal


    def roles(self, key, param):
        sql = """
            select val, name from access_data where code='ROLE'
        """;
        data_list = db.engine.execute(text(sql)).fetchall();
        filter_list = list(filter((lambda x: x['id'] != 'SUPER_ADMIN'), self.dataload(data_list)))
        return filter_list

    def codes(self, key, param):
        sql = """
            select val, name from access_data where code='CODE'
        """;
        data_list = db.engine.execute(text(sql)).fetchall();
        return self.dataload(data_list)