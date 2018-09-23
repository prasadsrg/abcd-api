from db import session, db
from sqlalchemy import text
from models.access_data_model import AccessDataModel
from mappers.access_data_mapper import AccessDataMapper
import datetime

class DataLoadService:
    session_info = None

    def dataload(self, results):
        returnVal = []
        for result in results:
            data = {'id': result[0], 'name': result[1]};
            returnVal.append(data)
        return returnVal


    def roles(self, key, param):
        sql = """
            select val, name from access_data where code='ROLE'
        """
        data_list = db.engine.execute(text(sql)).fetchall()
        filter_list = list(filter((lambda x: x['id'] != 'SUPER_ADMIN'), self.dataload(data_list)))
        return filter_list

    def codes(self, key, param):
        sql = """
            select val, name from access_data where code='CODE'
        """
        data_list = db.engine.execute(text(sql)).fetchall()
        return self.dataload(data_list)

    def branches(self, key, param):
        sql = """
            select id, name from branch where vid='{}'
        """.format(self.session_info['vid'])
        print(sql)
        data_list = db.engine.execute(text(sql)).fetchall()
        return self.dataload(data_list)