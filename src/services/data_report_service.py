from db import session, db
from sqlalchemy import text
import pyexcel as p
from flask import make_response, jsonify
import datetime

class DataReportService:
    session_info = None

    def consumers(self, key, param):

        sql = """
            select
            c.name as Name,
            c.mobile as Mobile,
            c.email as Email,
            c.aadhar as Aadhar,
            a.lane as Lane,
            a.land_mark as LandMark,
            a.city as City,
            a.state as State,
            a.country as Country,
            a.zipcode as Zipcode
            from consumer as c
            inner join address as a on (a.id = c.address_id);
            ) 
            """
        try:
            query_sets = db.engine.execute(text(sql)).fetchall()
            print(query_sets[0].items())
            if (len(query_sets)) != 0:
                res_data = [[i[0] for i in query_sets[0].items()]] + [list(i) for i in query_sets]
                sheet = p.Sheet(res_data)
                output = make_response(sheet.xls)
                output.headers["Content-Disposition"] = "attachment; filename=export.xls"
                output.headers["Content-type"] = "text/xls"
                return output
            else:
                res_json = {'status': 1, 'message': 'No Data found in the specified range'}
                return jsonify(res_json)
        except Exception as e:
            print(e)
            if e.args:
                res_data = e.args[0]
            else:
                res_data = e
            res_json = {'status': 0, 'error': res_data}
            return jsonify(res_json)