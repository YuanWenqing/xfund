# coding: utf8
from xfund.daos import models
from xfund.core.sqls import sql_handler


class FundDao:
    def __init__(self, sql: sql_handler.SqlHandler):
        self.sql = sql

    def _row_to_fund(self, row: dict):
        if row is None:
            return None
        return models.FundInfo(code=row['code'],
                               name=row['name'],
                               )

    def get_fund(self, code: str):
        query = 'select * from fund_nav where code=%s limit 1'
        args = [code]
        row = self.sql.do_select(query, args, size=None)
        return self._row_to_fund(row)
